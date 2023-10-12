# use lsof and get output 
# use ps -ef | grep <process name> and get output
import subprocess
from gandan import MMAP
def get_lsof_results(filename):
    """특정 파일에 대해 lsof의 실행 결과를 가져옵니다."""

    # lsof 명령을 실행하여 특정 파일을 열고 있는 프로세스 리스트를 가져옵니다.
    proc = subprocess.Popen(["lsof", filename], stdout=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    #COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
    # lsof의 출력을 파싱하여 프로세스 ID, 사용자 이름, 파일 유형, 파일 크기 등을 가져옵니다.
    results = []
    for i, line in enumerate(stdout.decode("utf-8").splitlines()):
        if i == 0:
            continue
        fields = line.split()
        if not fields[1] in results:
            results.append(fields[1])
    return results

if __name__ == "__main__":
    # 특정 파일을 열고 있는 프로세스 리스트를 가져옵니다.
    fpath = "/dev/shm/ORDER_FAKE.que"
    results = get_lsof_results(fpath)

    mm = MMAP(fpath, 1000, 1000)

    # 프로세스 리스트의 내용을 출력합니다.
    print(len(results))
    print(mm.count())