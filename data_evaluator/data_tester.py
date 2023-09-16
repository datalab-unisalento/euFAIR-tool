import reporter
from data_evaluator.non_specific import F,A, R
from utility.utility import myprint as mprint
import utility.utility as util
from utility.bcolors import bcolors as bc
import data_evaluator.csv_test as csv_


def percentage(value):
    return round(value[1]/value[0]*100, 2)


def data_evaluator(dataset_name, payload, link, method, id_europa):
    mprint("LOG: starting FINDABILITY test")
    res_F = F_(dataset_name, payload, link, method)
    mprint("LOG: starting ACCESSIBILITY test")
    res_A = A_(link)
    mprint("LOG: starting INTEROPERABILITY test")
    res_I = I_(dataset_name)
    mprint("LOG: starting REUSABILITY test")
    res_R = R_(payload, link, id_europa)

    return {"F": res_F, "A": res_A, "I" : res_I, "R": res_R}


def F_(dataset_name, payload, link, method):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO F:", bc.BLUE)

    mprint("METRICA F1:", bc.BLUE)
    try:
        f1 = F.F1(payload, link)
    except:
        print("ERRORE: in funzione f1")
        f1 = 1, 0
    mprint("PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%")
    
    mprint("METRICA F2:", bc.BLUE)
    try:
        f2 = F.F2(payload, link, method)
    except:
        print("ERRORE: in funzione f2")
        f2 = 1, 0
    mprint("PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%")

    mprint("METRICA F4:", bc.BLUE)
    try:
        f4 = F.F4(link)
    except:
        print("ERRORE: in funzione f4")
        f4 = 1, 0
    mprint("PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%")

    mprint("DATA QUALITY GUIDELINES:", bc.BLUE)
    try:
        if dataset_name.split(".")[-1] == "csv":
            dqgf = csv_.guidelines_f(dataset_name)
        else:
            dqgf = 1, 0
    except:
        print("ERRORE: in funzione dqgf")
        dqgf = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO F: " + str(round((dqgf[1] / dqgf[0] * 100), 2)) + "%", bc.BLUE)

    return {"F1": percentage(f1), "F2": percentage(f2), "F3": 0, "F4": percentage(f4), "GUIDELINES": percentage(dqgf)}


def A_(link):
    reporter.add_to_report("PRINCIPIO A")

    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO A:", bc.BLUE)

    mprint("METRICA A1:", bc.BLUE)
    try:
        a1 = A.A1(link)
    except:
        print("ERRORE: in funzione a1")
        a1 = 1, 0
    mprint("PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")
    
    mprint("METRICA A1_1:", bc.BLUE)
    try:
        a1_1 = A.A1_1()
    except:
        print("ERRORE: in funzione a1.1")
        a1_1 = 1, 0
    mprint("PUNTEGGIO METRICA A1_1 " + str(round((a1_1[1] / a1_1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1_1 " + str(round((a1_1[1] / a1_1[0] * 100), 2)) + "%")
    
    mprint("METRICA A1_2:", bc.BLUE)
    try:
        a1_2 = A.A1_2()
    except:
        print("ERRORE: in funzione a1.2")
        a1_2 = 1, 0
    mprint("PUNTEGGIO METRICA A1_2 " + str(round((a1_2[1] / a1_2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1_2 " + str(round((a1_2[1] / a1_2[0] * 100), 2)) + "%")

    return {"A1": percentage(a1), "A1.1": percentage(a1_1), "A1.2": percentage(a1_2), "A2": 0, "GUIDELINES": 0}


def I_(dataset_name):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO I:", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES:", bc.BLUE)
    try:
        if dataset_name.split(".")[-1] == "csv":
            dqgi = csv_.guidelines_i(dataset_name)
        else:
            dqgi = 1, 0
    except:
        print("ERRORE: in funzione dqgi")
        dqgi = 1, 0

    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO I: " + str(round((dqgi[1] / dqgi[0] * 100), 2)) + "%", bc.BLUE)

    return {"I1": 0, "I2": 0, "I3": 0, "GUIDELINES": percentage(dqgi)}


def R_(payload, link, id_europa):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO R:", bc.BLUE)

    mprint("METRICA R1_1:", bc.BLUE)
    try:
        r1_1 = R.R1_1(payload, link)
    except:
        print("ERRORE: in funzione r1.1")
        r1_1 = 1, 0
    mprint("PUNTEGGIO METRICA R1.1 " + str(round((r1_1[1] / r1_1[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1_2:", bc.BLUE)
    try:
        r1_2 = R.R1_2(payload, link)
    except:
        print("ERRORE: in funzione r1.2")
        r1_2 = 1, 0
    mprint("PUNTEGGIO METRICA R1.2 " + str(round((r1_2[1] / r1_2[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1:", bc.BLUE)
    try:
        r1_3 = R.R1_3(id_europa)
    except:
        print("ERRORE: in funzione r1.3")
        r1_3 = 1, 0
    mprint("PUNTEGGIO METRICA R1.3 " + str(round((r1_3[1] / r1_3[0] * 100), 2)) + "%", bc.BLUE)

    return {"R1": 0, "R1.1" : percentage(r1_1), "R1.2" : percentage(r1_2), "R1.3" : percentage(r1_3), "GUIDELINES": 0}




