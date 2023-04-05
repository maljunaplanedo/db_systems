import subprocess
from datetime import datetime, timedelta


def init():
    subprocess.call(['mongosh', '--quiet', 'clear.js'])
    subprocess.call(['./import.sh'])


def routine():
    begin = datetime.now()

    for step in range(100):
        subprocess.call(['mongosh', '--quiet', 'read2.js'], stdout=subprocess.DEVNULL)

    end = datetime.now()
    return (end - begin).total_seconds()


def create_index():
    subprocess.call(['mongosh', '--quiet', 'create_index.js'])


if __name__ == '__main__':
    with open('time_research_result.txt', 'w') as result:
        result.write(f'No index: {routine()}s\n')
        create_index()
        result.write(f'With index: {routine()}s\n')
