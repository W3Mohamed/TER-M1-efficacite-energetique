import subprocess
import time
import requests

LHM_URL = "http://localhost:8085/data.json"
CPU_POWER_ID = 29   # CPU Package Power
CPU_TEMP_ID = 15    # CPU Package Temperature
CPU_LOAD_ID = 23    # CPU Total Load

def get_sensor_value(sensor_id, unit):
    """Lit un capteur LibreHardwareMonitor et enlève son unité."""
    try:
        data = requests.get(LHM_URL, timeout=2).json()

        def find_sensor(node):
            if node.get("id") == sensor_id:
                val = node.get("Value", "0")
                val = val.replace(",", ".").replace(unit, "").strip()
                return float(val)

            for child in node.get("Children", []):
                result = find_sensor(child)
                if result is not None:
                    return result

        return find_sensor(data)

    except Exception as e:
        print(f"Erreur lecture capteur: {e}")
        return None


def get_cpu_power_watts():
    return get_sensor_value(CPU_POWER_ID, " W")


def get_cpu_temperature():
    return get_sensor_value(CPU_TEMP_ID, " °C")


def get_cpu_load():
    return get_sensor_value(CPU_LOAD_ID, " %")
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
    test_power = get_cpu_power_watts()
    test_temp = get_cpu_temperature()
    test_load = get_cpu_load()

    print("Test capteurs :")
    print(f"  Puissance CPU : {test_power}")
    print(f"  Température   : {test_temp}")
    print(f"  Charge CPU    : {test_load}")

    if test_power is None:
        print("ERREUR: Impossible de lire le capteur.")
        exit(1)
    
    matrix_versions = ["naive", "vector", "blocked", "parallel"]
    matrix_sizes = [1024]       # une taille
    fib_versions = ["fib_naive", "fib_iter", "fib_memo"]
    fib_sizes = [40]
    NB_RUNS = 2    # 2 répétitions par version
    
    all_results = []
    
    matrix_results = []
fib_results = []

# =========================
# Mesures pour les matrices
# =========================
for size in matrix_sizes:
    print(f"\n{'#'*60}")
    print(f"  MATRICES - TAILLE : {size}x{size}")
    print(f"{'#'*60}")
    for v in matrix_versions:
        run_energies = []
        run_times = []
        run_powers = []

        for run in range(NB_RUNS):
            print(f"\n  [Run {run+1}/{NB_RUNS}]", end="")
            r = measure_energy(v, size=size, sample_interval=0.05)
            run_energies.append(r["energy_j"])
            run_times.append(r["time_s"])
            run_powers.append(r["avg_power_w"])
            time.sleep(2)

        avg_e = sum(run_energies) / NB_RUNS
        avg_t = sum(run_times) / NB_RUNS
        avg_p = sum(run_powers) / NB_RUNS

        matrix_results.append({
            "size": size,
            "version": v,
            "avg_time_s": avg_t,
            "avg_power_w": avg_p,
            "avg_energy_j": avg_e
        })
        time.sleep(3)

# =========================
# Mesures pour Fibonacci
# =========================
for n in fib_sizes:
    print(f"\n{'#'*60}")
    print(f"  FIBONACCI - N : {n}")
    print(f"{'#'*60}")
    for v in fib_versions:
        run_energies = []
        run_times = []
        run_powers = []

        for run in range(NB_RUNS):
            print(f"\n  [Run {run+1}/{NB_RUNS}]", end="")
            r = measure_energy(v, size=n, sample_interval=0.05)
            run_energies.append(r["energy_j"])
            run_times.append(r["time_s"])
            run_powers.append(r["avg_power_w"])
            time.sleep(2)

        avg_e = sum(run_energies) / NB_RUNS
        avg_t = sum(run_times) / NB_RUNS
        avg_p = sum(run_powers) / NB_RUNS

        fib_results.append({
            "n": n,
            "version": v,
            "avg_time_s": avg_t,
            "avg_power_w": avg_p,
            "avg_energy_j": avg_e
        })
        time.sleep(3)
    
    # Résumé final
    print(f"\n{'='*90}")
print(f"{'RÉSUMÉ FINAL - MATRICES':^90}")
print(f"{'='*90}")
print(f"{'Taille':<8} {'Version':<12} {'Temps moy (s)':<16} {'Puissance moy (W)':<20} {'Énergie moy (J)'}")
print(f"{'-'*90}")
for r in matrix_results:
    print(f"{r['size']:<8} {r['version']:<12} {r['avg_time_s']:<16.3f} {r['avg_power_w']:<20.2f} {r['avg_energy_j']:.2f}")

print(f"\n{'='*90}")
print(f"{'RÉSUMÉ FINAL - FIBONACCI':^90}")
print(f"{'='*90}")
print(f"{'n':<8} {'Version':<12} {'Temps moy (s)':<16} {'Puissance moy (W)':<20} {'Énergie moy (J)'}")
print(f"{'-'*90}")
for r in fib_results:
    print(f"{r['n']:<8} {r['version']:<12} {r['avg_time_s']:<16.6f} {r['avg_power_w']:<20.2f} {r['avg_energy_j']:.2f}")