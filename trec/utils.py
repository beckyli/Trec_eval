import subprocess

def run_trec_eval(judgement_file_path, results_file_path):
    process = subprocess.Popen(['trec_eval', judgement_file_path,
                                results_file_path], stdout=subprocess.PIPE)
    map = p10 = p20 = None
    for line in process.stdout.read().split('\n'):
        if line.startswith('map'):
            map = line.split()[2]
        elif line.startswith('P_10'):
            p10 = line.split()[2]
        elif line.startswith('P_20'):
            p20 = line.split()[2]
    return map, p10, p20
