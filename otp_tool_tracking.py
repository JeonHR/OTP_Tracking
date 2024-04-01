import logging
import pyautogui
import psutil
import subprocess


# 로그 설정
logging.basicConfig(filename='popup_program.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
## file name
## logging은 inform 정도를 부여해서 log에 기록하는 용도

def check_txt_file(file_path, target_line):
    """
    특정 txt 파일에서 특정 라인을 확인하는 함수
    """
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1): #목적은 각 파일에 인덱스 값 부여하는 역할
                if line_number == target_line and "<LotID>" in line and ".00</LotID>" in line: # 특정 열의 해당 사항 있는 여부를 확인
                    return line # if 구문이 성공적으로 진행되었음을 알리는 것
        return None # 최종 값이 안나왔음을 알림
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None

def detect_popup(image_path):
    """
    팝업이 표시되었는지 감지하는 함수
    """
    return pyautogui.locateOnScreen(image_path) is not None

def is_program_running(program_name):
    """
    특정 프로그램이 실행 중인지 확인하는 함수
    """
    for proc in psutil.process_iter(['name']):
        if program_name.lower() in proc.info['name'].lower():
            return True
    return False

def run_program(program_path):
    """
    프로그램을 실행하는 함수
    """
    subprocess.Popen(program_path, shell=True)
    print("프로그램을 실행했습니다.")
    logging.info(f"프로그램을 실행했습니다: {program_path}")

if __name__ == "__main__":
    popup_image_path = "lot_end.PNG"       # 팝업 이미지 경로
    program_to_check = "20240227_OTP_Write3_Bin_Sort_1.2.0.exe"           # 체크할 프로그램 이름
    program_to_run = "C:/ENG/20240227_OTP_Write3_Bin_Sort_1.2.0/20240227_OTP_Write3_Bin_Sort_1.2.0.exe"     # 실행할 프로그램 경로
    txt_file_path = "C:/LitePoint/Tanami/lotSetup.xml"              # 특정 txt 파일 경로
    target_line = 4                          # 확인할 특정 라인 번호

    # 팝업이 표시되었는지 감지
    if detect_popup(popup_image_path):
        print("팝업이 감지되었습니다.")
        logging.info("팝업이 감지되었습니다.")
        # 특정 프로그램이 이미 실행 중인지 확인
        if not is_program_running(program_to_check):
            # 특정 라인에서 필요한 조건을 만족하는지 확인
            line = check_txt_file(txt_file_path, target_line)
            if line:
                print(f"파일에서 조건을 만족하는 라인을 찾았습니다: {line}")
                logging.info(f"파일에서 조건을 만족하는 라인을 찾았습니다: {line}")
                run_program(program_to_run)
            else:
                print(f"파일에서 조건을 만족하는 라인을 찾을 수 없습니다.")
                logging.info(f"파일에서 조건을 만족하는 라인을 찾을 수 없습니다.")
        else:
            print(f"{program_to_check} 프로그램이 이미 실행 중입니다.")
            logging.info(f"{program_to_check} 프로그램이 이미 실행 중입니다.")
    else:
        print("팝업이 감지되지 않았습니다.")
        
