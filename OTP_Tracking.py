import logging
import pyautogui
import psutil
import subprocess
import sys

def normalize_path(path):
    """
    파일 경로에서 슬래시를 사용하는 것을 일관되게 바꿔주는 함수
    """
    return path.replace('/', '\\')


def is_program_running_at_path(program_path):
    """
    특정 경로에 실행된 프로그램이 있는지 확인하는 함수
    """
    normalized_program_path = normalize_path(program_path)
    for proc in psutil.process_iter(['name', 'exe']):
    
        if proc.info['exe'] == normalized_program_path:
            return True
    return False

def detect_popup(image_path):
    """
    팝업이 표시되었는지 감지하는 함수
    """
    return pyautogui.locateOnScreen(image_path) is not None

def check_txt_file(file_path, target_line):
    """
    특정 txt 파일에서 특정 라인을 확인하는 함수
    """
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if line_number == target_line and "<LotID>" in line and ".00</LotID>" in line:
                return line
    return None

def run_program(program_path):
    """
    프로그램을 실행하는 함수
    """
    subprocess.Popen(program_path, shell=True)
    print("프로그램을 실행했습니다.")
    logging.info(f"프로그램을 실행했습니다: {program_path}")

if __name__ == "__main__":
    logging.basicConfig(filename='log_all.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    popup_image_path = "lot_end.PNG"       # 팝업 이미지 경로
    program_to_run = "D:/ENG/20240227_OTP_Write3_Bin_Sort_1.2.0/20240227_OTP_Write3_Bin_Sort_1.2.0.exe"    # 실행할 프로그램 경로
    program_to_run_path = "D:/LitePoint/Tanami/uwbOI.exe"  # 실행할 프로그램의 경로
    program_to_check = "20240227_OTP_Write3_Bin_Sort_1.2.0.exe"           # 체크할 프로그램 이름
    txt_file_path = "lotSetup.xml"              # 특정 txt 파일 경로
    target_line = 4                            # 확인할 특정 라인 번호

    # 팝업이 표시되었는지 감지
    if is_program_running_at_path(program_to_run_path):
        if detect_popup(popup_image_path):
            print("팝업이 감지되었습니다.")
            logging.info("팝업이 감지되었습니다.")

            if not is_program_running(program_to_check):
                # 특정 라인에서 필요한 조건을 만족하는지 확인
                line = check_txt_file(txt_file_path, target_line)
                if line:
                    print(f"파일에서 조건을 만족하는 라인을 찾았습니다: {line}")
                    logging.info(f"파일에서 조건을 만족하는 라인을 찾았습니다: {line}")
                    # 팝업이 감지된 후에 이미 실행된 프로그램이 없다면 실행
                    run_program(program_to_run)
                else:
                    print(f"파일에서 조건을 만족하는 라인을 찾을 수 없습니다.")
                    sys.exit()
            else:
                print(f"{program_to_check} 프로그램이 이미 실행 중입니다.")
                logging.info(f"{program_to_check} 프로그램이 이미 실행 중입니다.")
                sys.exit()
        else:
            print("팝업이 감지되지 않았습니다.")
            logging.info(f"팝업이 감지되지 않았습니다.")
            sys.exit()
    else:
        print(f"{program_to_run_path} 해당 프로그램은 대상이 아닙니다.")
        sys.exit()
