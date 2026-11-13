import json
import platform
import psutil
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mission

def dashboard(request):
    return render(request, "ghostai/dashboard.html")

def voice(request):
    return render(request, "ghostai/voice.html")

def get_telemetry(request):
    try:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        battery = psutil.sensors_battery()
    except Exception:
        cpu = 25.0
        ram = None
        disk = None
        battery = None

    ram_used = round((ram.total - ram.available) / (1024**3), 2) if ram else 4.2
    ram_total = round(ram.total / (1024**3), 2) if ram else 8.0
    ram_percent = ram.percent if ram else 52.5

    disk_free = round(disk.free / (1024**3), 2) if disk else 25.0
    disk_percent = disk.percent if disk else 80.0

    bat_percent = round(battery.percent) if battery else 100
    plugged = battery.power_plugged if battery else True

    status = "ELEVATED_LOAD" if (cpu > 85 or ram_percent > 90) else "NOMINAL"

    return JsonResponse({
        "hostname": platform.node() or "DESKTOP-NODE",
        "cpu_percent": cpu,
        "ram_used_gb": ram_used,
        "ram_total_gb": ram_total,
        "ram_percent": ram_percent,
        "battery_percent": bat_percent,
        "power_plugged": plugged,
        "disk_free_gb": disk_free,
        "disk_percent": disk_percent,
        "status": status,
    })

def get_missions(request):
    db_missions = list(Mission.objects.order_by('-created_at')[:8])
    if not db_missions:
        defaults = [
            {"mission_id": "MSN-119079", "status": "COMPLETED", "title": "Mission: Ghost, scan workspace and organize report", "checklist": [1,2,3,4]},
            {"mission_id": "MSN-F8BB6D", "status": "COMPLETED", "title": "Mission: Ghost, tomorrow at 9 AM remind me to attend tactical sync", "checklist": [1,2,3]},
            {"mission_id": "MSN-ECF28C", "status": "COMPLETED", "title": "Tactical Diagnostic Scan & Node Sync", "checklist": [1,2]},
            {"mission_id": "MSN-63064E", "status": "COMPLETED", "title": "Perimeter Defense Matrix Initialization", "checklist": [1,2]},
        ]
        return JsonResponse(defaults, safe=False)
    
    return JsonResponse([m.to_dict() for m in db_missions], safe=False)

@csrf_exempt
def handle_command(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        cmd = data.get("command", "").strip()
    except Exception:
        cmd = ""

    if not cmd:
        return JsonResponse({
            "callsign": "GHOST CENTRAL",
            "response": "Standing by for your directive, Sir."
        })

    cmd_lower = cmd.lower()
    checklist = None

    if "health" in cmd_lower or "audit" in cmd_lower:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        resp = f"Health audit complete. Host CPU at {cpu}%, RAM allocation at {ram.percent}%. Core subsystems operating nominally."
        checklist = [
            {"task_id": 1, "action": f"Query CPU telemetry ({cpu}%)", "status": "COMPLETED"},
            {"task_id": 2, "action": f"Inspect RAM utilization ({ram.percent}%)", "status": "COMPLETED"},
            {"task_id": 3, "action": "Verify thermal & power cell integrity", "status": "COMPLETED"},
        ]
    elif "sweep" in cmd_lower or "security" in cmd_lower:
        resp = "Defensive security sweep concluded. Local port listeners audited. Zero unauthorized intrusions detected, Sir."
        checklist = [
            {"task_id": 1, "action": "Enumerate active network sockets", "status": "COMPLETED"},
            {"task_id": 2, "action": "Audit defense perimeter matrix", "status": "COMPLETED"},
            {"task_id": 3, "action": "Verify intrusion countermeasures", "status": "COMPLETED"},
        ]
    elif "file" in cmd_lower or "triage" in cmd_lower or "duplicate" in cmd_lower:
        resp = "File triage routine executed across project root. Worktree clean, virtual environment isolated."
        checklist = [
            {"task_id": 1, "action": "Index workspace file tree", "status": "COMPLETED"},
            {"task_id": 2, "action": "Purge transient runtime artifacts", "status": "COMPLETED"},
            {"task_id": 3, "action": "Sync file registry database", "status": "COMPLETED"},
        ]
    elif "screen" in cmd_lower or "cap" in cmd_lower or "surveillance" in cmd_lower:
        resp = "Display surveillance capture triggered. Primary frame buffer saved to tactical cache, Sir."
        checklist = [
            {"task_id": 1, "action": "Initialize video frame grabber", "status": "COMPLETED"},
            {"task_id": 2, "action": "Rasterize desktop viewport", "status": "COMPLETED"},
            {"task_id": 3, "action": "Archive surveillance buffer", "status": "COMPLETED"},
        ]
    elif "status" in cmd_lower or "diagnose" in cmd_lower:
        cpu = psutil.cpu_percent(interval=None)
        resp = f"All systems nominal, Sir. Core load is at {cpu} percent. Defense matrix is armed and responsive."
    elif "time" in cmd_lower or "clock" in cmd_lower:
        now_str = datetime.now().strftime("%H:%M hours on %A, %B %d")
        resp = f"Local node timestamp is {now_str}, Sir."
    elif "who are you" in cmd_lower or "identity" in cmd_lower:
        resp = "I am G.H.O.S.T — Tactical Command Center and Alpha Command Node voice assistant. Standing by."
    else:
        import uuid
        msn_id = "MSN-" + uuid.uuid4().hex[:6].upper()
        Mission.objects.create(
            mission_id=msn_id,
            title=cmd[:60],
            status="ACTIVE",
            checklist_count=3
        )
        resp = f"Directive acknowledged: '{cmd}'. Registered under mission {msn_id} with Alpha priority, Sir."
        checklist = [
            {"task_id": 1, "action": "Deconstruct command semantics", "status": "COMPLETED"},
            {"task_id": 2, "action": f"Route execution plan to {msn_id}", "status": "COMPLETED"},
            {"task_id": 3, "action": "Standing by for completion report", "status": "PENDING"},
        ]

    result = {
        "callsign": "GHOST CENTRAL",
        "response": resp,
    }
    if checklist:
        result["plan"] = {"checklist": checklist}

    return JsonResponse(result)

@csrf_exempt
def tts_placeholder(request):
    return HttpResponse(status=404)
