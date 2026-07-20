#!/usr/bin/env python3
"""Compact reference runner for URR v0.1.0-native.

Finite diagnostic only. No quantum or relativity postulates are imported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml

VERSION = "0.1.0-native"


class URRError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code, self.message = code, message


def need(d: dict[str, Any], key: str, where: str = "root") -> Any:
    if key not in d:
        raise URRError("INVALID_SCHEMA", f"missing {where}.{key}")
    return d[key]


def vec(value: Any, n: int, name: str, *, positive=False, nonnegative=False) -> np.ndarray:
    x = np.full(n, float(value)) if np.isscalar(value) else np.asarray(value, float).reshape(-1)
    if x.size != n:
        raise URRError("DIMENSION_MISMATCH", f"{name}: {x.size} != {n}")
    if not np.all(np.isfinite(x)):
        raise URRError("NONFINITE_STATE", f"{name} is non-finite")
    if positive and np.any(x <= 0):
        raise URRError("INVALID_SCHEMA", f"{name} must be > 0")
    if nonnegative and np.any(x < 0):
        raise URRError("INVALID_SCHEMA", f"{name} must be >= 0")
    return x


def laplacian(graph: dict[str, Any]) -> np.ndarray:
    n = int(need(graph, "nodes", "graph"))
    W = np.zeros((n, n))
    for i, j, w in need(graph, "edges", "graph"):
        i, j, w = int(i), int(j), float(w)
        if not (0 <= i < n and 0 <= j < n and w >= 0):
            raise URRError("INVALID_SCHEMA", f"bad edge {(i, j, w)}")
        if i != j:
            W[i, j] += w
            W[j, i] += w
    return np.diag(W.sum(1)) - W


def grammar(cfg: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    L = laplacian(need(cfg, "graph"))
    fiber = need(cfg, "fiber")
    f = int(need(fiber, "dimension", "fiber"))
    C = np.asarray(need(fiber, "internal_operator", "fiber"), float)
    if C.shape != (f, f):
        raise URRError("DIMENSION_MISMATCH", "fiber.internal_operator")
    Gt = np.kron(L, np.eye(f)) + np.kron(np.eye(L.shape[0]), C)
    interaction = need(cfg, "grammar").get("interaction_operator")
    if interaction is not None:
        I = np.asarray(interaction, float)
        if I.shape != Gt.shape:
            raise URRError("DIMENSION_MISMATCH", "grammar.interaction_operator")
        Gt += I
    return L, Gt


def potential(cfg: dict[str, Any], n: int):
    if need(cfg, "type", "potential") != "polynomial_even":
        raise URRError("UNSUPPORTED_POTENTIAL", str(cfg.get("type")))
    k2, k4 = vec(need(cfg, "k2", "potential"), n, "k2"), vec(need(cfg, "k4", "potential"), n, "k4")
    value = lambda q: float(np.sum(0.5 * k2 * q**2 + 0.25 * k4 * q**4))
    grad = lambda q: k2 * q + k4 * q**3
    hess = lambda q: k2 + 3.0 * k4 * q**2
    return value, grad, hess


def evolve(cfg: dict[str, Any], Gt: np.ndarray) -> dict[str, Any]:
    dyn, init = need(cfg, "dynamics"), need(cfg, "initial_state")
    dt, steps, n = float(need(dyn, "dt", "dynamics")), int(need(dyn, "steps", "dynamics")), Gt.shape[0]
    if dt <= 0 or steps <= 0:
        raise URRError("INVALID_SCHEMA", "dt and steps must be positive")
    M = vec(need(dyn, "M", "dynamics"), n, "M", positive=True)
    D = vec(need(dyn, "D", "dynamics"), n, "D", nonnegative=True)
    K = float(need(dyn, "K", "dynamics"))
    V, grad, hess = potential(need(cfg, "potential"), n)
    source = need(cfg, "source")
    if need(source, "type", "source") != "constant":
        raise URRError("INVALID_SCHEMA", "only constant source is supported")
    J = vec(need(source, "value", "source"), n, "source.value")
    phi0, vphi0 = vec(need(init, "Phi", "initial_state"), n, "Phi"), vec(need(init, "Phi_velocity", "initial_state"), n, "Phi_velocity")
    psi0, vpsi0 = vec(need(init, "Psi", "initial_state"), n, "Psi"), vec(need(init, "Psi_velocity", "initial_state"), n, "Psi_velocity")
    phi_prev = phi0 - dt * vphi0 + 0.5 * dt**2 * (J - D*vphi0 - K*(Gt@phi0) - grad(phi0))/M
    psi_prev = psi0 - dt * vpsi0 + 0.5 * dt**2 * (D*vpsi0 - K*(Gt@psi0) - hess(phi0)*psi0)/M
    reader_den, mirror_den = M/dt**2 + D/(2*dt), M/dt**2 - D/(2*dt)
    if np.any(np.abs(reader_den) < 1e-14) or np.any(np.abs(mirror_den) < 1e-14):
        raise URRError("SINGULAR_UPDATE", "explicit recurrence denominator")
    phi, psi = np.zeros((steps+1, n)), np.zeros((steps+1, n))
    phi[0], psi[0] = phi0, psi0
    pm, sm = phi_prev, psi_prev
    for t in range(steps):
        p, s = phi[t], psi[t]
        pn = (2*M/dt**2*p - (M/dt**2-D/(2*dt))*pm - K*(Gt@p) - grad(p) + J)/reader_den
        sn = (2*M/dt**2*s - (M/dt**2+D/(2*dt))*sm - K*(Gt@s) - hess(p)*s)/mirror_den
        if not np.all(np.isfinite(pn)) or not np.all(np.isfinite(sn)):
            raise URRError("NONFINITE_STATE", f"step {t+1}")
        phi[t+1], psi[t+1], pm, sm = pn, sn, p, s
    pe, se = np.vstack([phi_prev, phi]), np.vstack([psi_prev, psi])
    rphi, rpsi, charge, action = [], [], [], 0.0
    for t in range(1, steps+1):
        p0, pp, px = pe[t-1], pe[t], pe[t+1]
        s0, sp, sx = se[t-1], se[t], se[t+1]
        rphi.append(M*(px-2*pp+p0)/dt**2 + D*(px-p0)/(2*dt) + K*(Gt@pp) + grad(pp) - J)
        rpsi.append(M*(sx-2*sp+s0)/dt**2 - D*(sx-s0)/(2*dt) + K*(Gt@sp) + hess(pp)*sp)
        vp, vs = (px-p0)/(2*dt), (sx-s0)/(2*dt)
        charge.append(float((M*vp)@vs + K*pp@Gt@sp + sp@grad(pp) - J@sp))
    for t in range(steps):
        dp, ds = phi[t+1]-phi[t], psi[t+1]-psi[t]
        action += float((M*dp)@ds/dt + 0.5*(phi[t]@(D*ds)-psi[t]@(D*dp)) - dt*(K*phi[t]@Gt@psi[t] + psi[t]@grad(phi[t]) - J@psi[t]))
    charge = np.asarray(charge)
    return {"phi":phi,"psi":psi,"M":M,"D":D,"K":K,"J":J,"dt":dt,"steps":steps,"V":V,
            "reader_residual":float(np.max(np.abs(rphi))),"mirror_residual":float(np.max(np.abs(rpsi))),
            "charge":charge,"charge_drift":float(np.max(np.abs(charge-charge[0]))/max(1.0,abs(float(charge[0])))),"action":action}


def tape(cfg: dict[str, Any], run: dict[str, Any]) -> dict[str, Any]:
    backend = need(cfg, "record_backend")
    mode = need(backend, "mode", "record_backend")
    if mode == "mirror":
        return {"status":"SKIPPED"}
    tc = need(backend, "tape", "record_backend")
    if need(tc, "gamma_policy", "record_backend.tape") == "from_D_over_M":
        gamma, bridge = float(np.mean(1-np.exp(-(run["D"]/run["M"])*run["dt"]))), "Dr"
    else:
        gamma, bridge = float(need(tc, "gamma", "record_backend.tape")), "user_declared"
    if not 0 <= gamma < 1:
        raise URRError("INVALID_SCHEMA", "tape gamma")
    phi = run["phi"]
    z = np.concatenate([phi[0], (phi[1]-phi[0])/run["dt"]])
    q0, stored, maxerr = float(z@z), 0.0, 0.0
    for _ in range(int(tc.get("steps", run["steps"]))):
        zn, rho = math.sqrt(1-gamma)*z, -math.sqrt(gamma)*z
        maxerr = max(maxerr, abs(float(zn@zn + rho@rho - z@z)))
        stored += float(rho@rho); z = zn
    return {"status":"EXECUTED","mode":mode,"gamma":gamma,"bridge_status":bridge,
            "max_step_conservation_error":maxerr,"total_conservation_error":abs(float(z@z+stored-q0)),"unified_action_claim":False}


def readouts(cfg: dict[str, Any], run: dict[str, Any], tol: float) -> list[dict[str, Any]]:
    phi, psi = run["phi"][-1], run["psi"][-1]; combined = np.r_[phi, psi]
    reports=[]
    for item in need(cfg, "readouts"):
        state, rid = need(item, "state", "readout"), need(item, "id", "readout")
        source = phi if state=="Phi" else psi if state=="Psi" else combined
        if "matrix" in item:
            A=np.asarray(item["matrix"],float)
        elif "selector" in item:
            A=np.zeros((1,source.size)); A[0,int(item["selector"])]=1
        else:
            A=np.eye(source.size)
        if A.ndim!=2 or A.shape[1]!=source.size:
            raise URRError("DIMENSION_MISMATCH", f"readout {rid}")
        pred=A@source; obs=vec(item.get("observed",np.zeros(pred.size)),pred.size,f"observed {rid}"); residual=pred-obs
        policy=need(item,"policy",f"readout {rid}")
        output = ({"prediction":pred.tolist(),"residual":residual.tolist()} if policy=="identity" else
                  float(np.linalg.norm(pred)) if policy=="norm" else float(np.mean(pred)) if policy=="mean" else
                  int(np.argmax(pred)) if policy=="argmax" else bool(pred[0]>=float(need(item,"threshold",f"readout {rid}"))))
        rank=int(np.linalg.matrix_rank(A,tol)); reports.append({"id":rid,"prediction":pred.tolist(),"observed":obs.tolist(),
            "residual":residual.tolist(),"policy_output":output,"rank":rank,"nullity":int(A.shape[1]-rank)})
    return reports


def information(cfg: dict[str, Any]) -> dict[str, Any]:
    info=need(cfg,"information"); raw=info.get("probabilities")
    if raw is None: return {"status":"NOT_COMPUTED","reason":"probability model missing"}
    p=np.asarray(raw,float)
    if np.any(p<0) or not np.isclose(p.sum(),1,atol=1e-12): raise URRError("INVALID_SCHEMA","probabilities")
    positive=p[p>0]; H=float(-np.sum(positive*np.log2(positive))); conv={}
    for unit in info.get("requested_conversions",[]):
        if unit=="bit": conv[unit]={"value":H,"unit":"bit"}
        elif unit=="byte": conv[unit]={"value":H/8,"unit":"byte"}
        elif unit=="nat": conv[unit]={"value":H*math.log(2),"unit":"nat"}
        elif unit=="hartley": conv[unit]={"value":H/math.log2(10),"unit":"hartley"}
        elif unit=="landauer_J":
            T=float(need(info,"temperature_K","information")); conv[unit]={"value":H*1.380649e-23*T*math.log(2),"unit":"J","temperature_K":T,"claim_status":"conditional_bridge","intrinsic_information_energy":False}
        else: raise URRError("INVALID_UNIT_BRIDGE",unit)
    idx=info.get("event_index"); self_info=None if idx is None else float(-math.log2(p[int(idx)]))
    return {"status":"COMPUTED","probabilities":p.tolist(),"entropy_rbit":H,"self_information_rbit":self_info,"conversions":conv}


def execute(config_path: Path, output: Path) -> dict[str, Any]:
    cfg=yaml.safe_load(config_path.read_text())
    for key in ("meta","ontology","units","graph","fiber","grammar","dynamics","potential","source","initial_state","record_backend","readouts","information","diagnostics","claim_policy","dag"): need(cfg,key)
    if cfg["meta"].get("native_only") is not True: raise URRError("INVALID_SCHEMA","meta.native_only")
    L,Gt=grammar(cfg); diag=need(cfg,"diagnostics")
    symmetry=float(np.max(np.abs(Gt-Gt.T))); rows=float(np.max(np.abs(L.sum(1))))
    if symmetry>float(diag.get("symmetry_tolerance",1e-10)) or rows>float(diag.get("row_sum_tolerance",1e-10)): raise URRError("INVALID_SCHEMA","operator gates")
    run=evolve(cfg,Gt); tr=tape(cfg,run); ro=readouts(cfg,run,float(diag.get("rank_tolerance",1e-10))); inf=information(cfg)
    failed=[]; warnings=[]
    if run["reader_residual"]>float(diag.get("reader_el_residual_tolerance",1e-8)): failed.append("EL_RESIDUAL_FAIL:reader")
    if run["mirror_residual"]>float(diag.get("mirror_el_residual_tolerance",1e-8)): failed.append("EL_RESIDUAL_FAIL:mirror")
    if run["charge_drift"]>float(diag.get("pairing_drift_warning",1e-2)): warnings.append("PAIRING_DRIFT_WARN")
    if tr.get("status")=="EXECUTED" and tr["total_conservation_error"]>float(diag.get("tape_conservation_tolerance",1e-12)): failed.append("tape_conservation")
    report={"meta":{"run_id":str(uuid.uuid4()),"timestamp_utc":datetime.now(timezone.utc).isoformat(),"runner_version":VERSION,"input_sha256":hashlib.sha256(config_path.read_bytes()).hexdigest(),"native_only":True},
      "operator":{"state_dimension":int(Gt.shape[0]),"laplacian_eigenvalues":np.linalg.eigvalsh(L).tolist(),"grammar_eigenvalues":np.linalg.eigvalsh(Gt).tolist(),"symmetry_error":symmetry,"laplacian_row_sum_error":rows},
      "dynamics":{"dt":run["dt"],"steps":run["steps"],"action":run["action"],"reader_el_residual_max":run["reader_residual"],"mirror_el_residual_max":run["mirror_residual"],"pairing_charge_initial":float(run["charge"][0]),"pairing_charge_final":float(run["charge"][-1]),"pairing_charge_relative_drift":run["charge_drift"],"potential_value_final":run["V"](run["phi"][-1])},
      "tape":tr,"readouts":ro,"information":inf,"claim":{"tier":"finite_diagnostic","verdict":"PASS" if not failed else "FAIL","failed_gates":failed,"warnings":warnings,"promotion_forbidden":True,"readout_is_truth_claim":False},
      "limitations":["linear DRL does not prove mechanistic handoff from Phi to Psi","tape has no unified DRL action","rbit physical conversions require an explicit bridge","quantum and relativity are outside the core"]}
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2,ensure_ascii=False)); np.savez_compressed(output.with_suffix(".npz"),phi=run["phi"],psi=run["psi"],pairing_charge=run["charge"],laplacian=L,universal_grammar=Gt)
    return report


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("config",type=Path); ap.add_argument("--output",type=Path,default=Path("urr_run_report.json")); args=ap.parse_args()
    try: report=execute(args.config,args.output)
    except URRError as exc:
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps({"claim":{"tier":"finite_diagnostic","verdict":"FAIL","error_code":exc.code,"error_message":exc.message}},indent=2)); print(exc.code,exc.message); return 2
    print(json.dumps({"verdict":report["claim"]["verdict"],"tier":report["claim"]["tier"],"reader_el_residual_max":report["dynamics"]["reader_el_residual_max"],"mirror_el_residual_max":report["dynamics"]["mirror_el_residual_max"],"pairing_charge_relative_drift":report["dynamics"]["pairing_charge_relative_drift"],"output":str(args.output)},indent=2)); return 0 if report["claim"]["verdict"]=="PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
