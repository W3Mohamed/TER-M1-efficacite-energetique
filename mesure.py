import subprocess
import time
import requests

LHM_URL = "http://localhost:8085/data.json"
CPU_SENSOR_ID = 11  # CPU Package Power

def get_cpu_power_watts():
    """Lit la puissance CPU réelle depuis LibreHardwareMonitor"""
    try:
        data = requests.get(LHM_URL, timeout=2).json()
        
        def find_sensor(node, target_id):
            if node.get("id") == target_id:
                val = node.get("Value", "0").replace(",", ".").replace(" W", "").strip()
                return float(val)
            for child in node.get("Children", []):
                result = find_sensor(child, target_id)
                if result is not None:
                    return result
        
        return find_sensor(data, target_id=CPU_SENSOR_ID)
    except Exception as e:
        print(f"Erreur lecture capteur: {e}")
        return None

def measure_energy(version, size=1024, sample_interval=0.1):
    """
    Mesure l'énergie réelle consommée pendant l'exécution du benchmark Rust.
    Échantillonne la puissance toutes les `sample_interval` secondes.
    Energie (Joules) = somme de P(t) * dt
    """
    print(f"\n{'='*50}")
    print(f"Mesure version : {version} | Taille : {size}")
    print(f"{'='*50}")
    
    power_samples = []
    timestamps = []
    
    # Lancer le processus Rust
    process = subprocess.Popen(
        [r".\target\release\ter-m1-efficacite-energetique.exe", version, str(size)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    start_time = time.time()
    
    # Échantillonner la puissance pendant l'exécution
    while process.poll() is None:
        watts = get_cpu_power_watts()
        t = time.time() - start_time
        if watts is not None:
            power_samples.append(watts)
            timestamps.append(t)
            print(f"  t={t:.2f}s -> {watts:.2f} W")
        time.sleep(sample_interval)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Lire la sortie Rust
    stdout, _ = process.communicate()
    rust_output = stdout.decode("utf-8", errors="ignore").strip()
    
    # Calcul de l'énergie par intégration trapézoïdale
    if len(power_samples) >= 2:
        energy_joules = 0.0
        for i in range(1, len(power_samples)):
            dt = timestamps[i] - timestamps[i-1]
            avg_power = (power_samples[i] + power_samples[i-1]) / 2
            energy_joules += avg_power * dt
    elif len(power_samples) == 1:
        energy_joules = power_samples[0] * total_time
    else:
        energy_joules = 0.0
    
    avg_power = sum(power_samples) / len(power_samples) if power_samples else 0
    
    print(f"\n  Résultat Rust     : {rust_output}")
    print(f"  Temps total       : {total_time:.3f} s")
    print(f"  Puissance moyenne : {avg_power:.2f} W")
    print(f"  Énergie consommée : {energy_joules:.2f} J")
    
    return {
        "version": version,
        "time_s": total_time,
        "avg_power_w": avg_power,
        "energy_j": energy_joules,
        "samples": len(power_samples)
    }

if __name__ == "__main__":
    test = get_cpu_power_watts()
    if test is None:
        print("ERREUR: Impossible de lire le capteur.")
        exit(1)
    print(f"Capteur OK — Puissance actuelle : {test:.2f} W")
    
    versions = ["naive", "vector", "blocked", "parallel"]
    sizes = [1024]       # une taille
    NB_RUNS = 2               # 2 répétitions par version
    
    all_results = []
    
    for size in sizes:
        print(f"\n{'#'*60}")
        print(f"  TAILLE : {size}x{size}")
        print(f"{'#'*60}")
        for v in versions:
            run_energies = []
            run_times = []
            for run in range(NB_RUNS):
                print(f"\n  [Run {run+1}/{NB_RUNS}]", end="")
                r = measure_energy(v, size=size, sample_interval=0.05)
                run_energies.append(r["energy_j"])
                run_times.append(r["time_s"])
                time.sleep(2)
            
            avg_e = sum(run_energies) / NB_RUNS
            avg_t = sum(run_times) / NB_RUNS
            all_results.append({
                "size": size,
                "version": v,
                "avg_time_s": avg_t,
                "avg_energy_j": avg_e
            })
            time.sleep(3)
    
    # Résumé final
    print(f"\n{'='*65}")
    print(f"{'RÉSUMÉ FINAL (moyennes sur 3 runs)':^65}")
    print(f"{'='*65}")
    print(f"{'Taille':<8} {'Version':<12} {'Temps moy (s)':<16} {'Énergie moy (J)'}")
    print(f"{'-'*65}")
    for r in all_results:
        print(f"{r['size']:<8} {r['version']:<12} {r['avg_time_s']:<16.3f} {r['avg_energy_j']:.2f}")