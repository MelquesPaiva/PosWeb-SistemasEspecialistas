from chat.chat import find_prescription_by_keys

if __name__ == "__main__":
    prescriptions = find_prescription_by_keys(["Nanofactor", "Ácido"])
    print(prescriptions)