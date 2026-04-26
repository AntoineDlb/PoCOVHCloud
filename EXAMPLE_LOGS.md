# Exemples de logs pour tester le PoC

## 1. Kernel Panic (CRITIQUE)

```
[CRITICAL] 2026-04-26T19:45:12.234Z kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)
[CRITICAL] 2026-04-26T19:45:12.456Z CPU0: Package temperature/speed normal
[CRITICAL] 2026-04-26T19:45:12.678Z systemd[1]: Caught signal SEGV.
[CRITICAL] 2026-04-26T19:45:12.890Z systemd[1]: Spawning emergency shell.
[ERROR] 2026-04-26T19:45:13.012Z Emergency shell will be executed
```

## 2. Disque plein (CRITIQUE)

```
[ERROR] 2026-04-26T19:50:22.123Z df: filesystem /var is 99% full (8.9GB/9.0GB used)
[ERROR] 2026-04-26T19:50:22.234Z write failed: No space left on device
[ERROR] 2026-04-26T19:50:22.345Z application[2541]: Cannot write to database: errno=28 ENOSPC
[WARN] 2026-04-26T19:50:22.456Z systemd: Failed to write to system journal
[CRITICAL] 2026-04-26T19:50:22.567Z /srv/logs/nginx.log.old cannot be rotated: disk full
```

## 3. Problème réseau (MAJEUR)

```
[WARN] 2026-04-26T20:01:05.123Z eth0: Link down
[ERROR] 2026-04-26T20:01:05.234Z Cannot reach gateway 192.168.1.1
[ERROR] 2026-04-26T20:01:05.345Z DNS resolver timeout: nameserver 8.8.8.8
[WARN] 2026-04-26T20:01:05.456Z application[1234]: Connection pool exhausted
[WARN] 2026-04-26T20:01:05.567Z nginx: upstream timeout (backend server 10.0.0.5:8080)
```

## 4. Latence élevée (MAJEUR)

```
[WARN] 2026-04-26T20:15:30.123Z application: API response time p95=2450ms (threshold=500ms)
[WARN] 2026-04-26T20:15:30.234Z mysql: slow query 3.45s: SELECT * FROM users WHERE id=123
[WARN] 2026-04-26T20:15:30.345Z redis: response time 450ms (expected <50ms)
[WARN] 2026-04-26T20:15:30.456Z systemd: Service startup timeout after 90s
[INFO] 2026-04-26T20:15:30.567Z load average: 12.5 (4 CPUs) - high system load
```

## 5. Ressources CPU saturées (MAJEUR)

```
[WARN] 2026-04-26T20:30:15.123Z CPU0: freq 2.4GHz, temp 87C (critical threshold: 90C)
[WARN] 2026-04-26T20:30:15.234Z CPU1: freq 2.4GHz, temp 85C
[WARN] 2026-04-26T20:30:15.345Z process[5678] kworker: consuming 95% CPU
[INFO] 2026-04-26T20:30:15.456Z context switches: 50000/sec (normal: 5000/sec)
[WARN] 2026-04-26T20:30:15.567Z system load: 28.5 (4 cores available)
```

## 6. Mémoire insuffisante (MAJEUR)

```
[WARN] 2026-04-26T20:45:00.123Z Memory: 15.8GB/16GB (98% utilization)
[ERROR] 2026-04-26T20:45:00.234Z process[3456]: out of memory - OOM killer invoked
[ERROR] 2026-04-26T20:45:00.345Z Killed process java[3456]: score 843
[WARN] 2026-04-26T20:45:00.456Z Swap usage: 2.3GB (filesystem may become full)
[ERROR] 2026-04-26T20:45:00.567Z malloc failed: Cannot allocate 512MB
```

## 7. Température disque haute (MINEUR)

```
[WARN] 2026-04-26T21:00:30.123Z sda: Temperature 65C (warning: 60C, critical: 70C)
[INFO] 2026-04-26T21:00:30.234Z sda: Power-On Hours 12456
[WARN] 2026-04-26T21:00:30.345Z sda: Reallocated Sector Count increased (SMART health: PASSED)
[INFO] 2026-04-26T21:00:30.456Z Thermal throttling may occur if temperature exceeds 70C
```

## 8. Service arrêté (MINEUR)

```
[ERROR] 2026-04-26T21:15:45.123Z systemd: Unit nginx.service entered failed state
[ERROR] 2026-04-26T21:15:45.234Z nginx[2345]: bind() to 0.0.0.0:80 failed: Address already in use
[INFO] 2026-04-26T21:15:45.345Z systemd: Attempted restart - retries 1/3
[WARN] 2026-04-26T21:15:45.456Z Application will wait 30 seconds before next retry
```

## 9. Erreur d'authentification (MINEUR)

```
[WARN] 2026-04-26T21:30:00.123Z sshd[4567]: Invalid user admin from 203.0.113.45
[WARN] 2026-04-26T21:30:00.234Z sshd[4567]: Failed password for invalid user admin from 203.0.113.45
[WARN] 2026-04-26T21:30:00.345Z sshd: 5 more authentication failures; logfile not rotated
[INFO] 2026-04-26T21:30:00.456Z systemd-logind: Failed to authorize user for remote seat
```

## 10. Avertissement général système (INFO)

```
[INFO] 2026-04-26T21:45:15.123Z Security update available: kernel 5.15.0-94 -> 5.15.0-95
[INFO] 2026-04-26T21:45:15.234Z Scheduled reboot pending (system uptime 125 days)
[INFO] 2026-04-26T21:45:15.345Z systemd: Unit update-notifier.service completed
[WARN] 2026-04-26T21:45:15.456Z Certificate expires in 30 days: certbot renewal due
```

---

## Instructions d'utilisation

1. Copie l'un des exemples ci-dessus (le contenu entre les trois backticks ` ``` `)
2. Colle-le dans le champ **Log d'erreur serveur** de l'application Streamlit
3. Clique sur le bouton **Analyser l'incident**
4. L'application retournera:
   - **Criticité**: CRITIQUE, MAJEUR, MINEUR ou INFO
   - **Résumé technique**: 2 phrases maximum en français
   - **Plan d'action**: 3 étapes de résolution
