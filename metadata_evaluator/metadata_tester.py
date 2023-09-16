import utility as util
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc
from metadata_evaluator import F_europa, A_europa, I_europa, R_europa, F_italia, A_italia, I_italia, R_italia, \
    F_generic, A_generic, I_generic, R_generic
import reporter


def percentage(value):
    return round(value[1] / value[0] * 100, 2)


def metadata_evaluator_europa(dataset_id, method, payload):
    reporter.add_to_report("METADATA EUROPA")

    mprint("LOG: starting FINDABILITY test")
    res_F = F_europa_(payload, method)
    mprint("LOG: starting ACCESSIBILITY test")
    res_A = A_europa_(payload)
    mprint("LOG: starting INTEROPERABILITY test")
    res_I = I_europa_(dataset_id, payload)
    mprint("LOG: starting REUSABILITY test")
    res_R = R_europa_(payload)
    return {"F": res_F, "A": res_A, "I": res_I, "R": res_R}


def F_europa_(payload, method):
    reporter.add_to_report("PRINCIPIO F")

    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO F:", bc.BLUE)

    mprint("METRICA F1:", bc.BLUE)
    try:
        f1 = F_europa.F1(payload)
    except Exception as e:
        print("ERRORE: in funzione f1", e)
        f1 = 1, 0
    mprint("PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%")

    mprint("METRICA F2:", bc.BLUE)
    try:
        f2 = F_europa.F2(payload, method)
    except Exception as e:
        print("ERRORE: in funzione 2", e)
        f2 = 1, 0
    mprint("PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%")

    mprint("METRICA F3:", bc.BLUE)
    try:
        f3 = F_europa.F3(payload)
    except Exception as e:
        print("ERRORE: in funzione f3", e)
        f3 = 1, 0
    mprint("PUNTEGGIO METRICA F3 " + str(round((f3[1] / f3[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F3 " + str(round((f3[1] / f3[0] * 100), 2)) + "%")

    mprint("METRICA F4:", bc.BLUE)
    try:
        f4 = F_europa.F4(payload)
    except Exception as e:
        print("ERRORE: in funzione f4", e)
        f4 = 1, 0
    mprint("PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%")

    f_max_point = round(f1[0] + f2[0] + f3[0] + f4[0], 2)
    f_scored_point = round(f1[1] + f2[1] + f3[1] + f4[1], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO F: " + str(f_scored_point) + "/" + str(f_max_point) + "->"
           + str((round(f_scored_point / f_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgf = F_europa.guidelines_f(payload)
    except Exception as e:
        print("ERRORE: in funzione dqgf", e)
        dqgf = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO F: " + str(round((dqgf[1] / dqgf[0] * 100), 2)) + "%", bc.BLUE)

    return {"F1": percentage(f1), "F2": percentage(f2), "F3": percentage(f3), "F4": percentage(f4),
            "GUIDELINES": percentage(dqgf)}


def A_europa_(payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO A:", bc.BLUE)

    mprint("METRICA A1:", bc.BLUE)
    try:
        a1 = A_europa.A1()
    except Exception as e:
        print("ERRORE: in funzione a1", e)
        a1 = 1, 0
    mprint("PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")

    mprint("METRICA A1.1:", bc.BLUE)
    try:
        a1_1 = A_europa.A1_1()
    except Exception as e:
        print("ERRORE: in funzione a1.1", e)
        a1_1 = 1, 0
    mprint("PUNTEGGIO METRICA A1 " + str(round((a1_1[1] / a1_1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")

    mprint("METRICA A1:", bc.BLUE)
    try:
        a1_2 = A_europa.A1_2()
    except Exception as e:
        print("ERRORE: in funzione a1.2", e)
        a1_2 = 1, 0
    mprint("PUNTEGGIO METRICA A1 " + str(round((a1_2[1] / a1_2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")

    mprint("METRICA A2:", bc.BLUE)
    try:
        a2 = A_europa.A2()
    except Exception as e:
        print("ERRORE: in funzione a2", e)
        a2 = 1, 0
    mprint("PUNTEGGIO METRICA A2 " + str(round((a2[1] / a2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A2 " + str(round((a2[1] / a2[0] * 100), 2)) + "%")

    a_max_point = round(a1[0] + a2[0], 2)
    a_scored_point = round(a1[1] + a2[1], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO A: " + str(a_scored_point) + "/" + str(a_max_point) + "->"
           + str((round(a_scored_point / a_max_point * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO TOTALE PRINCIPIO A: " + str(a_scored_point) + "/" + str(a_max_point) + "->"
                           + str((round(a_scored_point / a_max_point * 100), 2)) + "%")

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqga = A_europa.guidelines_a(payload)
    except Exception as e:
        print("ERRORE: in funzione a2", e)
        dqga = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO A: " + str(round(dqga[1], 2)) + "/" + str(round(dqga[0])) + "->"
           + str(round((dqga[1] / dqga[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO A: " + str(round(dqga[1], 2)) + "/" +
                           str(round(dqga[0])) + "->" + str(round((dqga[1] / dqga[0] * 100), 2)) + "%")

    return {"A1": percentage(a1), "A1.1": percentage(a1_1), "A1.2": percentage(a1_2),
            "A2": percentage(a2), "GUIDELINES": percentage(dqga)}


def I_europa_(dataset_id, payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO I:", bc.BLUE)

    mprint("METRICA I1:", bc.BLUE)
    try:
        i1 = I_europa.I1()
    except Exception as e:
        print("ERRORE: in funzione i1", e)
        i1 = 1, 0
    mprint("PUNTEGGIO METRICA I1 " + str(round((i1[1] / i1[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA I2:", bc.BLUE)
    try:
        i2 = I_europa.I2(payload)
    except Exception as e:
        print("ERRORE: in funzione i2", e)
        i2 = 1, 0
    mprint("PUNTEGGIO METRICA I2 " + str(round((i2[1] / i2[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA I3:", bc.BLUE)
    try:
        i3 = I_europa.I3(payload)
    except Exception as e:
        print("ERRORE: in funzione i3", e)
        i3 = 1, 0
    mprint("PUNTEGGIO METRICA I3 " + str(round((i3[1] / i3[0] * 100), 2)) + "%", bc.BLUE)

    i_max_point = round(i1[0] + i2[0] + i3[0], 2)
    i_scored_point = round(i1[1] + i2[1] + i3[0], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO I: " + str(i_scored_point) + "/" + str(i_max_point) + "->"
           + str((round(i_scored_point / i_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgi = I_europa.guidelines_i(dataset_id)
    except Exception as e:
        print("ERRORE: in funzione dqgi", e)
        dqgi = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO I: " + str(round(dqgi[1], 2)) + "/" + str(round(dqgi[0])) + "->"
           + str(round((dqgi[1] / dqgi[0] * 100), 2)) + "%", bc.BLUE)

    return {"I1": percentage(i1), "I2": percentage(i2), "I3": percentage(i3), "GUIDELINES": percentage(dqgi)}


def R_europa_(payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO R:", bc.BLUE)

    mprint("METRICA R1:", bc.BLUE)
    try:
        r1 = R_europa.R1()
    except Exception as e:
        print("ERRORE: in funzione r1", e)
        r1 = 1, 0
    mprint("PUNTEGGIO METRICA R1 " + str(round((r1[1] / r1[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1_1:", bc.BLUE)
    try:
        r1_1 = R_europa.R1_1(payload)
    except Exception as e:
        print("ERRORE: in funzione r1.1", e)
        r1_1 = 1, 0
    mprint("PUNTEGGIO METRICA R1.1 " + str(round((r1_1[1] / r1_1[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1_2:", bc.BLUE)
    try:
        r1_2 = R_europa.R1_2(payload)
    except Exception as e:
        print("ERRORE: in funzione r1.2", e)
        r1_2 = 1, 0
    mprint("PUNTEGGIO METRICA R1.2 " + str(round((r1_2[1] / r1_2[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1:", bc.BLUE)
    try:
        r1_3 = R_europa.R1_3(payload)
    except Exception as e:
        print("ERRORE: in funzione r1.3", e)
        r1_3 = 1, 0
    mprint("PUNTEGGIO METRICA R1.3 " + str(round((r1_3[1] / r1_3[0] * 100), 2)) + "%", bc.BLUE)

    r_max_point = round(r1[0] + r1_1[0] + r1_2[0] + r1_3[0], 2)
    r_scored_point = round(r1[1] + r1_1[1] + r1_2[1] + r1_3[0], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO I: " + str(r_scored_point) + "/" + str(r_max_point) + "->"
           + str((round(r_scored_point / r_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgr = R_europa.guidelines_r(payload)
    except Exception as e:
        print("ERRORE: in funzione dqgr", e)
        dqgr = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO R: " + str(round(dqgr[1], 2)) + "/" + str(round(dqgr[0])) + "->"
           + str(round((dqgr[1] / dqgr[0] * 100), 2)) + "%", bc.BLUE)

    return {"R1": percentage(r1), "R1.1": percentage(r1_1), "R1.2": percentage(r1_2), "R1.3": percentage(r1_3),
            "GUIDELINES": percentage(dqgr)}


def metadata_evaluator_italia(dataset_id, method, payload, eu_dataset_id, caller):
    reporter.add_to_report("METADATA ITALIA")

    mprint("LOG: starting FINDABILITY test")
    res_F = F_italia_(payload, method, caller)
    mprint("LOG: starting ACCESSIBILITY test")
    res_A = A_italia_(payload)
    mprint("LOG: starting INTEROPERABILITY test")
    res_I = I_italia_(dataset_id, payload)
    mprint("LOG: starting REUSABILITY test")
    res_R = R_italia_(payload, eu_dataset_id)
    # f1, f2, f3, f4,
    return {"F": res_F, "A": res_A, "I": res_I, "R": res_R}


def F_italia_(payload, method, caller):
    reporter.add_to_report("PRINCIPIO F EUROPA")

    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO F:", bc.BLUE)

    mprint("METRICA F1:", bc.BLUE)
    try:
        f1 = F_italia.F1(payload)
    except:
        print("ERRORE: in funzione f1")
        f1 = 1, 0
    mprint("PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%")

    mprint("METRICA F2:", bc.BLUE)
    try:
        f2 = F_italia.F2(payload, method)
    except:
        print("ERRORE: in funzione f2")
        f2 = 1, 0
    mprint("PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%")

    mprint("METRICA F3:", bc.BLUE)
    try:
        f3 = F_italia.F3(payload)
    except:
        print("ERRORE: in funzione f3")
        f3 = 1, 0
    mprint("PUNTEGGIO METRICA F3 " + str(round((f3[1] / f3[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F3 " + str(round((f3[1] / f3[0] * 100), 2)) + "%")

    mprint("METRICA F4:", bc.BLUE)
    try:
        f4 = F_italia.F4(payload, caller)
    except:
        print("ERRORE: in funzione f4")
        f4 = 1, 0
    mprint("PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%")

    f_max_point = round(f1[0] + f2[0] + f3[0] + f4[0], 2)
    f_scored_point = round(f1[1] + f2[1] + f3[1] + f4[1], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO F: " + str(f_scored_point) + "/" + str(f_max_point) + "->"
           + str((round(f_scored_point / f_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgf = F_italia.guidelines_f(payload)
    except:
        print("ERRORE: in funzione dqgf")
        dqgf = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO F: " + str(round((dqgf[1] / dqgf[0] * 100), 2)) + "%", bc.BLUE)

    return {"F1": percentage(f1), "F2": percentage(f2), "F3": percentage(f3), "F4": percentage(f4),
            "GUIDELINES": percentage(dqgf)}


def A_italia_(payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO A:", bc.BLUE)

    mprint("METRICA A1:", bc.BLUE)
    try:
        a1 = A_italia.A1()
    except:
        print("ERRORE: in funzione a1")
        a1 = 1, 0
    mprint("PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")

    mprint("METRICA A1.1:", bc.BLUE)
    try:
        a1_1 = A_italia.A1_1()
    except:
        print("ERRORE: in funzione a1.1")
        a1_1 = 1, 0
    mprint("PUNTEGGIO METRICA A1 " + str(round((a1_1[1] / a1_1[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")

    mprint("METRICA A1.2:", bc.BLUE)
    try:
        a1_2 = A_italia.A1_2()
    except:
        print("ERRORE: in funzione a1.2")
        a1_2 = 1, 0
    mprint("PUNTEGGIO METRICA A1 " + str(round((a1_2[1] / a1_2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")

    mprint("METRICA A2:", bc.BLUE)
    try:
        a2 = A_italia.A2()
    except:
        print("ERRORE: in funzione a2")
        a2 = 1, 0
    mprint("PUNTEGGIO METRICA A2 " + str(round((a2[1] / a2[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO METRICA A2 " + str(round((a2[1] / a2[0] * 100), 2)) + "%")

    a_max_point = round(a1[0] + a2[0], 2)
    a_scored_point = round(a1[1] + a2[1], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO A: " + str(a_scored_point) + "/" + str(a_max_point) + "->"
           + str((round(a_scored_point / a_max_point * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO TOTALE PRINCIPIO A: " + str(a_scored_point) + "/" + str(a_max_point) + "->"
                           + str((round(a_scored_point / a_max_point * 100), 2)) + "%")

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqga = A_italia.guidelines_a(payload)
    except:
        print("ERRORE: in funzione dqga")
        dqga = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO A: " + str(round(dqga[1], 2)) + "/" + str(round(dqga[0])) + "->"
           + str(round((dqga[1] / dqga[0] * 100), 2)) + "%", bc.BLUE)
    reporter.add_to_report("--" + "PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO A: " + str(round(dqga[1], 2)) + "/" +
                           str(round(dqga[0])) + "->" + str(round((dqga[1] / dqga[0] * 100), 2)) + "%")

    return {"A1": percentage(a1), "A1.1": percentage(a1_1), "A1.2": percentage(a1_2),
            "A2": percentage(a2), "GUIDELINES": percentage(dqga)}


def I_italia_(dataset_id, payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO I:", bc.BLUE)

    mprint("METRICA I1:", bc.BLUE)
    try:
        i1 = I_italia.I1()
    except:
        print("ERRORE: in funzione i1")
        i1 = 1, 0
    mprint("PUNTEGGIO METRICA I1 " + str(round((i1[1] / i1[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA I2:", bc.BLUE)
    try:
        i2 = I_italia.I2(payload)
    except:
        print("ERRORE: in funzione i2")
        i2 = 1, 0
    mprint("PUNTEGGIO METRICA I2 " + str(round((i2[1] / i2[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA I3:", bc.BLUE)
    try:
        i3 = I_italia.I3(payload)
    except:
        print("ERRORE: in funzione i3")
        i3 = 1, 0
    mprint("PUNTEGGIO METRICA I3 " + str(round((i3[1] / i3[0] * 100), 2)) + "%", bc.BLUE)

    i_max_point = round(i1[0] + i2[0] + i3[0], 2)
    i_scored_point = round(i1[1] + i2[1] + i3[0], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO I: " + str(i_scored_point) + "/" + str(i_max_point) + "->"
           + str((round(i_scored_point / i_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgi = I_italia.guidelines_i(dataset_id)
    except:
        print("ERRORE: in funzione dqgi")
        dqgi = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO I: " + str(round(dqgi[1], 2)) + "/" + str(round(dqgi[0])) + "->"
           + str(round((dqgi[1] / dqgi[0] * 100), 2)) + "%", bc.BLUE)

    return {"I1": percentage(i1), "I2": percentage(i2), "I3": percentage(i3), "GUIDELINES": percentage(dqgi)}


def R_italia_(payload, eu_dataset_id):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO R:", bc.BLUE)

    mprint("METRICA R1:", bc.BLUE)
    try:
        r1 = R_italia.R1()
    except:
        print("ERRORE: in funzione r1")
        r1 = 1, 0
    mprint("PUNTEGGIO METRICA R1 " + str(round((r1[1] / r1[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1_1:", bc.BLUE)
    try:
        r1_1 = R_italia.R1_1(payload)
    except:
        print("ERRORE: in funzione r1.1")
        r1_1 = 1, 0
    mprint("PUNTEGGIO METRICA R1.1 " + str(round((r1_1[1] / r1_1[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1_2:", bc.BLUE)
    try:
        r1_2 = R_italia.R1_2(payload)
    except:
        print("ERRORE: in funzione r1.2")
        r1_2 = 1, 0
    mprint("PUNTEGGIO METRICA R1.2 " + str(round((r1_2[1] / r1_2[0] * 100), 2)) + "%", bc.BLUE)

    mprint("METRICA R1:", bc.BLUE)
    try:
        r1_3 = R_italia.R1_3(eu_dataset_id)
    except:
        print("ERRORE: in funzione r1.3")
        r1_3 = 1, 0
    mprint("PUNTEGGIO METRICA R1.3 " + str(round((r1_3[1] / r1_3[0] * 100), 2)) + "%", bc.BLUE)

    r_max_point = round(r1[0] + r1_1[0] + r1_2[0] + r1_3[0], 2)
    r_scored_point = round(r1[1] + r1_1[1] + r1_2[1] + r1_3[0], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO I: " + str(r_scored_point) + "/" + str(r_max_point) + "->"
           + str((round(r_scored_point / r_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgr = R_italia.guidelines_r(payload)
    except:
        print("ERRORE: in funzione dqgr")
        dqgr = 1, 0
    mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO R: " + str(round(dqgr[1], 2)) + "/" + str(round(dqgr[0])) + "->"
           + str(round((dqgr[1] / dqgr[0] * 100), 2)) + "%", bc.BLUE)

    return {"R1": percentage(r1), "R1.1": percentage(r1_1), "R1.2": percentage(r1_2), "R1.3": percentage(r1_3),
            "GUIDELINES": percentage(dqgr)}


def metadata_evaluator_generic(dataset_id, method, payload, dataset_url):
    reporter.add_to_report("METADATA ITALIA")

    mprint("LOG: starting FINDABILITY test")
    res_F = F_generic_(payload, method, dataset_id)
    mprint("LOG: starting ACCESSIBILITY test")
    res_A = A_generic_(payload)
    mprint("LOG: starting INTEROPERABILITY test")
    res_I = I_generic_(dataset_id, dataset_url, payload)
    mprint("LOG: starting REUSABILITY test")
    res_R = R_generic_(payload)
    # f1, f2, f3, f4,
    return {"F": res_F, "A": res_A, "I": res_I, "R": res_R}


def F_generic_(payload, method, dataset_id):
    reporter.add_to_report("PRINCIPIO F EUROPA")

    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO F:", bc.BLUE)

    mprint("METRICA F1:", bc.BLUE)
    try:
        f1 = F_generic.F1(payload, dataset_id)
        mprint("PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%", bc.BLUE)
        reporter.add_to_report("--" + "PUNTEGGIO METRICA F1 " + str(round((f1[1] / f1[0] * 100), 2)) + "%")
    except:
        print("F1 failed")
        f1 = 1, 0

    mprint("METRICA F2:", bc.BLUE)
    try:
        f2 = F_generic.F2(payload, method)
        mprint("PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%", bc.BLUE)
        reporter.add_to_report("--" + "PUNTEGGIO METRICA F2 " + str(round((f2[1] / f2[0] * 100), 2)) + "%")
    except:
        print("F2 failed")
        f2 = 1, 0

    mprint("METRICA F3:", bc.BLUE)
    try:
        f3 = F_generic.F3(payload)
        mprint("PUNTEGGIO METRICA F3 " + str(round((f3[1] / f3[0] * 100), 2)) + "%", bc.BLUE)
        reporter.add_to_report("--" + "PUNTEGGIO METRICA F3 " + str(round((f3[1] / f3[0] * 100), 2)) + "%")
    except:
        print("F3 failed")
        f3 = 1, 0

    mprint("METRICA F4:", bc.BLUE)
    try:
        f4 = F_generic.F4(payload)
        mprint("PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%", bc.BLUE)
        reporter.add_to_report("--" + "PUNTEGGIO METRICA F4 " + str(round((f4[1] / f4[0] * 100), 2)) + "%")
    except:
        print("F4 failed")
        f4 = 1, 0

    f_max_point = round(f1[0] + f2[0] + f3[0] + f4[0], 2)
    f_scored_point = round(f1[1] + f2[1] + f3[1] + f4[1], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO F: " + str(f_scored_point) + "/" + str(f_max_point) + "->"
           + str((round(f_scored_point / f_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgf = F_generic.guidelines_f(payload)
        mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO F: " + str(round((dqgf[1] / dqgf[0] * 100), 2)) + "%",
               bc.BLUE)
    except:
        print("dqgf failed")
        dqgf = 1, 0

    return {"F1": percentage(f1), "F2": percentage(f2), "F3": percentage(f3), "F4": percentage(f4),
            "GUIDELINES": percentage(dqgf)}


def A_generic_(payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO A:", bc.BLUE)

    mprint("METRICA A1:", bc.BLUE)
    try:
        a1 = A_generic.A1()
        mprint("PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%", bc.BLUE)
        reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")
    except:
        print("A1 failed")
        a1 = 1, 0

    mprint("METRICA A1.1:", bc.BLUE)
    try:
        a1_1 = A_generic.A1_1()
        mprint("PUNTEGGIO METRICA A1 " + str(round((a1_1[1] / a1_1[0] * 100), 2)) + "%", bc.BLUE)
        reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")
    except:
        print("A11 failed")
        a1_1 = 1, 0

    mprint("METRICA A1:", bc.BLUE)
    try:
        a1_2 = A_generic.A1_2()
        mprint("PUNTEGGIO METRICA A1 " + str(round((a1_2[1] / a1_2[0] * 100), 2)) + "%", bc.BLUE)
        # reporter.add_to_report("--" + "PUNTEGGIO METRICA A1 " + str(round((a1[1] / a1[0] * 100), 2)) + "%")
    except:
        print("A12 failed")
        a1_2 = 1, 0

    mprint("METRICA A2:", bc.BLUE)
    try:
        a2 = A_generic.A2()
        mprint("PUNTEGGIO METRICA A2 " + str(round((a2[1] / a2[0] * 100), 2)) + "%", bc.BLUE)
        # reporter.add_to_report("--" + "PUNTEGGIO METRICA A2 " + str(round((a2[1] / a2[0] * 100), 2)) + "%")
    except:
        print("A2 failed")
        a2 = 1, 0

    a_max_point = round(a1[0] + a2[0], 2)
    a_scored_point = round(a1[1] + a2[1], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO A: " + str(a_scored_point) + "/" + str(a_max_point) + "->"
           + str((round(a_scored_point / a_max_point * 100), 2)) + "%", bc.BLUE)
    # reporter.add_to_report("--" + "PUNTEGGIO TOTALE PRINCIPIO A: " + str(a_scored_point) + "/" + str(a_max_point) + "->"
    #        + str((round(a_scored_point / a_max_point * 100), 2)) + "%")

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqga = A_generic.guidelines_a(payload)
        mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO A: " + str(round(dqga[1], 2)) + "/" + str(
            round(dqga[0])) + "->"
               + str(round((dqga[1] / dqga[0] * 100), 2)) + "%", bc.BLUE)
        # reporter.add_to_report("--" + "PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO A: " + str(round(dqga[1], 2)) + "/" +
        #                        str(round(dqga[0])) + "->" + str(round((dqga[1] / dqga[0] * 100), 2)) + "%")
    except:
        print("dqga failed")
        dqga = 1, 0

    return {"A1": percentage(a1), "A1.1": percentage(a1_1), "A1.2": percentage(a1_2),
            "A2": percentage(a2), "GUIDELINES": percentage(dqga)}


def I_generic_(dataset_id, dataset_url, payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO I:", bc.BLUE)

    mprint("METRICA I1:", bc.BLUE)
    try:
        i1 = I_generic.I1()
        mprint("PUNTEGGIO METRICA I1 " + str(round((i1[1] / i1[0] * 100), 2)) + "%", bc.BLUE)
    except:
        print("I1 failed")
        i1 = 1, 0

    mprint("METRICA I2:", bc.BLUE)
    try:
        i2 = I_generic.I2(payload)
        mprint("PUNTEGGIO METRICA I2 " + str(round((i2[1] / i2[0] * 100), 2)) + "%", bc.BLUE)
    except Exception as e:
        print("I1 failed", e)
        i2 = 1, 0

    mprint("METRICA I3:", bc.BLUE)
    try:
        i3 = I_generic.I3(payload, dataset_url)
        mprint("PUNTEGGIO METRICA I3 " + str(round((i3[1] / i3[0] * 100), 2)) + "%", bc.BLUE)
    except Exception as e:
        print("I3 failed", e)
        i3 = 1, 0

    i_max_point = round(i1[0] + i2[0] + i3[0], 2)
    i_scored_point = round(i1[1] + i2[1] + i3[0], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO I: " + str(i_scored_point) + "/" + str(i_max_point) + "->"
           + str((round(i_scored_point / i_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgi = I_generic.guidelines_i(dataset_id)
        mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO I: " + str(round(dqgi[1], 2)) + "/" + str(
            round(dqgi[0])) + "->"
               + str(round((dqgi[1] / dqgi[0] * 100), 2)) + "%", bc.BLUE)
    except:
        print("dqgi failed")
        dqgi = 1, 0

    return {"I1": percentage(i1), "I2": percentage(i2), "I3": percentage(i3), "GUIDELINES": percentage(dqgi)}


def R_generic_(payload):
    util.aline(bc.BLUE)
    util.aline(bc.BLUE)
    mprint("CRITERIO R:", bc.BLUE)

    mprint("METRICA R1:", bc.BLUE)
    try:
        r1 = R_generic.R1()
        mprint("PUNTEGGIO METRICA R1 " + str(round((r1[1] / r1[0] * 100), 2)) + "%", bc.BLUE)
    except:
        print("R1 failed")
        r1 = 1, 0

    mprint("METRICA R1_1:", bc.BLUE)
    try:
        r1_1 = R_generic.R1_1(payload)
        mprint("PUNTEGGIO METRICA R1.1 " + str(round((r1_1[1] / r1_1[0] * 100), 2)) + "%", bc.BLUE)
    except Exception as e:
        print("R11 failed", e)
        r1_1 = 1, 0

    mprint("METRICA R1_2:", bc.BLUE)
    try:
        r1_2 = R_generic.R1_2(payload)
        mprint("PUNTEGGIO METRICA R1.2 " + str(round((r1_2[1] / r1_2[0] * 100), 2)) + "%", bc.BLUE)
    except:
        print("R12 failed")
        r1_2 = 1, 0

    mprint("METRICA R1:", bc.BLUE)
    try:
        r1_3 = R_generic.R1_3(payload)
        mprint("PUNTEGGIO METRICA R1.3 " + str(round((r1_3[1] / r1_3[0] * 100), 2)) + "%", bc.BLUE)
    except:
        print("R13 failed")
        r1_3 = 1, 0

    r_max_point = round(r1[0] + r1_1[0] + r1_2[0] + r1_3[0], 2)
    r_scored_point = round(r1[1] + r1_1[1] + r1_2[1] + r1_3[0], 2)
    mprint("PUNTEGGIO TOTALE PRINCIPIO I: " + str(r_scored_point) + "/" + str(r_max_point) + "->"
           + str((round(r_scored_point / r_max_point * 100), 2)) + "%", bc.BLUE)

    mprint("DATA QUALITY GUIDELINES", bc.BLUE)
    try:
        dqgr = R_generic.guidelines_r(payload)
        mprint("PUNTEGGIO DATA QUALITY GUIDELINES PRINCIPIO R: " + str(round(dqgr[1], 2)) + "/" + str(
            round(dqgr[0])) + "->"
               + str(round((dqgr[1] / dqgr[0] * 100), 2)) + "%", bc.BLUE)
    except:
        print("dqgr failed")
        dqgr = 1, 0

    return {"R1": percentage(r1), "R1.1": percentage(r1_1), "R1.2": percentage(r1_2), "R1.3": percentage(r1_3),
            "GUIDELINES": percentage(dqgr)}
