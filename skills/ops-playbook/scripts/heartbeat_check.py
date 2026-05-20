#!/usr/bin/env python3
"""
Heartbeat self-check — no_agent script (no LLM overhead).
Checks system health and writes to /root/HEARTBEAT.md

Usage: python3 heartbeat_check.py
Run via cron as: no_agent: true, script: heartbeat_check.py

Replaces the LLM-driven heartbeat job (6 calls/day → 0 tokens).
"""
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import re


def get_meminfo():
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        mem = {}
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0].rstrip(':')
                val = int(parts[1])  # KB
                mem[key] = val
        total = mem.get('MemTotal', 0) / 1024  # MB
        avail = mem.get('MemAvailable', 0) / 1024  # MB
        pct = (avail / total * 100) if total else 0
        return avail, total, pct
    except:
        return 0, 0, 0


def get_load():
    try:
        with open('/proc/loadavg', 'r') as f:
            return f.read().split()[0:3]
    except:
        return ['?', '?', '?']


def check_failed_auth():
    try:
        result = subprocess.run(['journalctl', '--since', '24 hours ago', '-n', '9999'],
                              capture_output=True, text=True, timeout=10)
        failed = [l for l in result.stdout.split('\n')
                  if 'Failed password' in l or 'Failed publickey' in l]
        return len(failed)
    except:
        return 0


def check_processes():
    procs = {}
    for fn in ['hindsight-api', 'hermes-gateway', 'node', 'python3']:
        try:
            result = subprocess.run(['pgrep', '-f', fn], capture_output=True, text=True)
            count = len([x for x in result.stdout.strip().split('\n') if x])
            if count > 0:
                procs[fn] = count
        except:
            pass
    return procs


def check_docker():
    try:
        result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}'],
                              capture_output=True, text=True, timeout=10)
        return [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
    except:
        return []


def check_fail2ban():
    try:
        result = subprocess.run(['fail2ban-client', 'status'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'Jail list' in line:
                    return line.strip()
        return 'fail2ban: unknown'
    except:
        return 'fail2ban: not running'


def check_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            secs = float(f.read().split()[0])
        days = int(secs // 86400)
        hrs = int((secs % 86400) // 3600)
        mins = int((secs % 3600) // 60)
        return f"{days}d {hrs}h {mins}m"
    except:
        return '?'


def check_scale_grove():
    """Flag ScaleGrove decision if >7 days old."""
    decisions_file = Path('/root/.hermes/memory/decisions/scale_grove_contract.txt')
    if decisions_file.exists():
        try:
            content = decisions_file.read_text()
            match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
            if match:
                date_str = match.group(1)
                decision_date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                age = (datetime.now(timezone.utc) - decision_date).days
                if age > 7:
                    return f"⚠️ ScaleGrove: {age} days old — needs follow-up"
        except:
            pass
    return None


if __name__ == '__main__':
    avail, total, mem_pct = get_meminfo()
    load = get_load()
    failed_auth = check_failed_auth()
    procs = check_processes()
    containers = check_docker()
    fail2ban = check_fail2ban()
    uptime = check_uptime()
    scale_grove_flag = check_scale_grove()

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    warnings = []

    if mem_pct < 20:
        warnings.append(f"⚠️ Memory low: {mem_pct:.0f}% available")
    if scale_grove_flag:
        warnings.append(scale_grove_flag)

    status = '⚠️ Attention needed' if warnings else '✅ All clear'

    lines = [
        f"# Heartbeat\n",
        f"**Last run:** {now}\n",
        f"**Status:** {status}\n",
        f"\n",
        f"## System\n",
        f"- Memory: **{mem_pct:.0f}%** free (~{avail:.0f}MB of ~{total:.0f}MB)\n",
        f"- Load: **{', '.join(load)}**\n",
        f"- Uptime: **{uptime}**\n",
        f"- Processes: **{procs}**\n",
        f"\n",
        f"## Containers\n",
        f"- Running: **{containers}**\n",
        f"\n",
        f"## Security\n",
        f"- fail2ban: {fail2ban}\n",
        f"- Failed auth (24h): **{failed_auth}**\n",
        f"\n",
    ]
    if warnings:
        lines.append("## Warnings\n")
        for w in warnings:
            lines.append(f"- {w}\n")
    else:
        lines.append("## All clear.\n")

    Path('/root/HEARTBEAT.md').write_text(''.join(lines))
    print(f"Updated HEARTBEAT.md — {status}")
    if warnings:
        for w in warnings:
            print(f"  {w}")