def guard__accept_init__TO__accept_S2(model_info):
    return (not model_info['p4'])
def guard__accept_init__TO__accept_S3(model_info):
    return (not model_info['p4'] and not model_info['p6'])
def guard__accept_init__TO__accept_S4(model_info):
    return (1)
def guard__accept_init__TO__accept_S5(model_info):
    return (not model_info['p6'])
def guard__accept_init__TO__accept_S6(model_info):
    return (not model_info['p2'] and not model_info['p4'])
def guard__accept_init__TO__accept_S7(model_info):
    return (not model_info['p2'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_init__TO__accept_S8(model_info):
    return (not model_info['p2'])
def guard__accept_init__TO__accept_S9(model_info):
    return (not model_info['p2'] and not model_info['p6'])
def guard__accept_init__TO__accept_S10(model_info):
    return (not model_info['p0'] and not model_info['p4'])
def guard__accept_init__TO__accept_S11(model_info):
    return (not model_info['p0'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_init__TO__accept_S12(model_info):
    return (not model_info['p0'])
def guard__accept_init__TO__accept_S13(model_info):
    return (not model_info['p0'] and not model_info['p6'])
def guard__accept_init__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'])
def guard__accept_init__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_init__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'])
def guard__accept_init__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p6'])
def guard__accept_S2__TO__accept_S2(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S2__TO__accept_S3(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S2__TO__accept_S4(model_info):
    return (model_info['p1'] and model_info['p3'] and model_info['p7'])
def guard__accept_S2__TO__accept_S5(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S2__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S2__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S2__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p7'])
def guard__accept_S2__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S2__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S2__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S2__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and model_info['p7'])
def guard__accept_S2__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S2__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S2__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S2__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p7'])
def guard__accept_S2__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S3__TO__accept_S2(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'])
def guard__accept_S3__TO__accept_S3(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S3__TO__accept_S4(model_info):
    return (model_info['p1'] and model_info['p3'])
def guard__accept_S3__TO__accept_S5(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p6'])
def guard__accept_S3__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'])
def guard__accept_S3__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S3__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'])
def guard__accept_S3__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p6'])
def guard__accept_S3__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'])
def guard__accept_S3__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S3__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'])
def guard__accept_S3__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p6'])
def guard__accept_S3__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'])
def guard__accept_S3__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S3__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'])
def guard__accept_S3__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p6'])
def guard__accept_S4__TO__accept_S2(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_S3(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S4__TO__accept_S4(model_info):
    return (model_info['p1'] and model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_S5(model_info):
    return (model_info['p1'] and model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S4__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S4__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S4__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S4__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S4__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S4__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S4__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S5__TO__accept_S2(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S5__TO__accept_S3(model_info):
    return (model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S5__TO__accept_S4(model_info):
    return (model_info['p1'] and model_info['p3'] and model_info['p5'])
def guard__accept_S5__TO__accept_S5(model_info):
    return (model_info['p1'] and model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S5__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S5__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S5__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'])
def guard__accept_S5__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S5__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S5__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S5__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and model_info['p5'])
def guard__accept_S5__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S5__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S5__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S5__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'])
def guard__accept_S5__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S6__TO__accept_S2(model_info):
    return (model_info['p1'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S6__TO__accept_S3(model_info):
    return (model_info['p1'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S6__TO__accept_S4(model_info):
    return (model_info['p1'] and model_info['p7'])
def guard__accept_S6__TO__accept_S5(model_info):
    return (model_info['p1'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S6__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S6__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S6__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p7'])
def guard__accept_S6__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S6__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S6__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S6__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p7'])
def guard__accept_S6__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S6__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S6__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S6__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p7'])
def guard__accept_S6__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S7__TO__accept_S2(model_info):
    return (model_info['p1'] and not model_info['p4'])
def guard__accept_S7__TO__accept_S3(model_info):
    return (model_info['p1'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S7__TO__accept_S4(model_info):
    return (model_info['p1'])
def guard__accept_S7__TO__accept_S5(model_info):
    return (model_info['p1'] and not model_info['p6'])
def guard__accept_S7__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'])
def guard__accept_S7__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S7__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'])
def guard__accept_S7__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p6'])
def guard__accept_S7__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'])
def guard__accept_S7__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S7__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'])
def guard__accept_S7__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p6'])
def guard__accept_S7__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'])
def guard__accept_S7__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S7__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'])
def guard__accept_S7__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p6'])
def guard__accept_S8__TO__accept_S2(model_info):
    return (model_info['p1'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_S3(model_info):
    return (model_info['p1'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S8__TO__accept_S4(model_info):
    return (model_info['p1'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_S5(model_info):
    return (model_info['p1'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S8__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S8__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S8__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S8__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S8__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S8__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p5'] and model_info['p7'])
def guard__accept_S8__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S9__TO__accept_S2(model_info):
    return (model_info['p1'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S9__TO__accept_S3(model_info):
    return (model_info['p1'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S9__TO__accept_S4(model_info):
    return (model_info['p1'] and model_info['p5'])
def guard__accept_S9__TO__accept_S5(model_info):
    return (model_info['p1'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S9__TO__accept_S6(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S9__TO__accept_S7(model_info):
    return (model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S9__TO__accept_S8(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p5'])
def guard__accept_S9__TO__accept_S9(model_info):
    return (model_info['p1'] and not model_info['p2'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S9__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S9__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S9__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p5'])
def guard__accept_S9__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p1'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S9__TO__accept_S14(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S9__TO__accept_init(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S9__TO__accept_S15(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p5'])
def guard__accept_S9__TO__accept_S16(model_info):
    return (not model_info['p0'] and model_info['p1'] and not model_info['p2'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S10__TO__accept_S2(model_info):
    return (model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S10__TO__accept_S3(model_info):
    return (model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S10__TO__accept_S4(model_info):
    return (model_info['p3'] and model_info['p7'])
def guard__accept_S10__TO__accept_S5(model_info):
    return (model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S10__TO__accept_S6(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S10__TO__accept_S7(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S10__TO__accept_S8(model_info):
    return (not model_info['p2'] and model_info['p3'] and model_info['p7'])
def guard__accept_S10__TO__accept_S9(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S10__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S10__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S10__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p3'] and model_info['p7'])
def guard__accept_S10__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S10__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S10__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S10__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and model_info['p7'])
def guard__accept_S10__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S11__TO__accept_S2(model_info):
    return (model_info['p3'] and not model_info['p4'])
def guard__accept_S11__TO__accept_S3(model_info):
    return (model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S11__TO__accept_S4(model_info):
    return (model_info['p3'])
def guard__accept_S11__TO__accept_S5(model_info):
    return (model_info['p3'] and not model_info['p6'])
def guard__accept_S11__TO__accept_S6(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'])
def guard__accept_S11__TO__accept_S7(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S11__TO__accept_S8(model_info):
    return (not model_info['p2'] and model_info['p3'])
def guard__accept_S11__TO__accept_S9(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p6'])
def guard__accept_S11__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'])
def guard__accept_S11__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S11__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p3'])
def guard__accept_S11__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p6'])
def guard__accept_S11__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'])
def guard__accept_S11__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and not model_info['p6'])
def guard__accept_S11__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'])
def guard__accept_S11__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p6'])
def guard__accept_S12__TO__accept_S2(model_info):
    return (model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_S3(model_info):
    return (model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S12__TO__accept_S4(model_info):
    return (model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_S5(model_info):
    return (model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S12__TO__accept_S6(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_S7(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S12__TO__accept_S8(model_info):
    return (not model_info['p2'] and model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_S9(model_info):
    return (not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S12__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S12__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S12__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S12__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and model_info['p7'])
def guard__accept_S12__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S13__TO__accept_S2(model_info):
    return (model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S13__TO__accept_S3(model_info):
    return (model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S13__TO__accept_S4(model_info):
    return (model_info['p3'] and model_info['p5'])
def guard__accept_S13__TO__accept_S5(model_info):
    return (model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S13__TO__accept_S6(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S13__TO__accept_S7(model_info):
    return (not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S13__TO__accept_S8(model_info):
    return (not model_info['p2'] and model_info['p3'] and model_info['p5'])
def guard__accept_S13__TO__accept_S9(model_info):
    return (not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S13__TO__accept_S10(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S13__TO__accept_S11(model_info):
    return (not model_info['p0'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S13__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p3'] and model_info['p5'])
def guard__accept_S13__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S13__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S13__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S13__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and model_info['p5'])
def guard__accept_S13__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p3'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S14__TO__accept_S2(model_info):
    return (not model_info['p4'] and model_info['p7'])
def guard__accept_S14__TO__accept_S3(model_info):
    return (not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S14__TO__accept_S4(model_info):
    return (model_info['p7'])
def guard__accept_S14__TO__accept_S5(model_info):
    return (not model_info['p6'] and model_info['p7'])
def guard__accept_S14__TO__accept_S6(model_info):
    return (not model_info['p2'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S14__TO__accept_S7(model_info):
    return (not model_info['p2'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S14__TO__accept_S8(model_info):
    return (not model_info['p2'] and model_info['p7'])
def guard__accept_S14__TO__accept_S9(model_info):
    return (not model_info['p2'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S14__TO__accept_S10(model_info):
    return (not model_info['p0'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S14__TO__accept_S11(model_info):
    return (not model_info['p0'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S14__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p7'])
def guard__accept_S14__TO__accept_S13(model_info):
    return (not model_info['p0'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S14__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'] and model_info['p7'])
def guard__accept_S14__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S14__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p7'])
def guard__accept_S14__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S2(model_info):
    return (not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_S3(model_info):
    return (not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S4(model_info):
    return (model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_S5(model_info):
    return (model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S6(model_info):
    return (not model_info['p2'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_S7(model_info):
    return (not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S8(model_info):
    return (not model_info['p2'] and model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_S9(model_info):
    return (not model_info['p2'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S10(model_info):
    return (not model_info['p0'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_S11(model_info):
    return (not model_info['p0'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S15__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p5'] and model_info['p7'])
def guard__accept_S15__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p5'] and not model_info['p6'] and model_info['p7'])
def guard__accept_S16__TO__accept_S2(model_info):
    return (not model_info['p4'] and model_info['p5'])
def guard__accept_S16__TO__accept_S3(model_info):
    return (not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S16__TO__accept_S4(model_info):
    return (model_info['p5'])
def guard__accept_S16__TO__accept_S5(model_info):
    return (model_info['p5'] and not model_info['p6'])
def guard__accept_S16__TO__accept_S6(model_info):
    return (not model_info['p2'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S16__TO__accept_S7(model_info):
    return (not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S16__TO__accept_S8(model_info):
    return (not model_info['p2'] and model_info['p5'])
def guard__accept_S16__TO__accept_S9(model_info):
    return (not model_info['p2'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S16__TO__accept_S10(model_info):
    return (not model_info['p0'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S16__TO__accept_S11(model_info):
    return (not model_info['p0'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S16__TO__accept_S12(model_info):
    return (not model_info['p0'] and model_info['p5'])
def guard__accept_S16__TO__accept_S13(model_info):
    return (not model_info['p0'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S16__TO__accept_S14(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'])
def guard__accept_S16__TO__accept_init(model_info):
    return (not model_info['p0'] and not model_info['p2'] and not model_info['p4'] and model_info['p5'] and not model_info['p6'])
def guard__accept_S16__TO__accept_S15(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p5'])
def guard__accept_S16__TO__accept_S16(model_info):
    return (not model_info['p0'] and not model_info['p2'] and model_info['p5'] and not model_info['p6'])

STATE_TRANS = {
    'accept_init' : {
        (guard__accept_init__TO__accept_S2, 'accept_S2'),
        (guard__accept_init__TO__accept_S3, 'accept_S3'),
        (guard__accept_init__TO__accept_S4, 'accept_S4'),
        (guard__accept_init__TO__accept_S5, 'accept_S5'),
        (guard__accept_init__TO__accept_S6, 'accept_S6'),
        (guard__accept_init__TO__accept_S7, 'accept_S7'),
        (guard__accept_init__TO__accept_S8, 'accept_S8'),
        (guard__accept_init__TO__accept_S9, 'accept_S9'),
        (guard__accept_init__TO__accept_S10, 'accept_S10'),
        (guard__accept_init__TO__accept_S11, 'accept_S11'),
        (guard__accept_init__TO__accept_S12, 'accept_S12'),
        (guard__accept_init__TO__accept_S13, 'accept_S13'),
        (guard__accept_init__TO__accept_S14, 'accept_S14'),
        (guard__accept_init__TO__accept_init, 'accept_init'),
        (guard__accept_init__TO__accept_S15, 'accept_S15'),
        (guard__accept_init__TO__accept_S16, 'accept_S16'),
    },
    'accept_S2' : {
        (guard__accept_S2__TO__accept_S2, 'accept_S2'),
        (guard__accept_S2__TO__accept_S3, 'accept_S3'),
        (guard__accept_S2__TO__accept_S4, 'accept_S4'),
        (guard__accept_S2__TO__accept_S5, 'accept_S5'),
        (guard__accept_S2__TO__accept_S6, 'accept_S6'),
        (guard__accept_S2__TO__accept_S7, 'accept_S7'),
        (guard__accept_S2__TO__accept_S8, 'accept_S8'),
        (guard__accept_S2__TO__accept_S9, 'accept_S9'),
        (guard__accept_S2__TO__accept_S10, 'accept_S10'),
        (guard__accept_S2__TO__accept_S11, 'accept_S11'),
        (guard__accept_S2__TO__accept_S12, 'accept_S12'),
        (guard__accept_S2__TO__accept_S13, 'accept_S13'),
        (guard__accept_S2__TO__accept_S14, 'accept_S14'),
        (guard__accept_S2__TO__accept_init, 'accept_init'),
        (guard__accept_S2__TO__accept_S15, 'accept_S15'),
        (guard__accept_S2__TO__accept_S16, 'accept_S16'),
    },
    'accept_S3' : {
        (guard__accept_S3__TO__accept_S2, 'accept_S2'),
        (guard__accept_S3__TO__accept_S3, 'accept_S3'),
        (guard__accept_S3__TO__accept_S4, 'accept_S4'),
        (guard__accept_S3__TO__accept_S5, 'accept_S5'),
        (guard__accept_S3__TO__accept_S6, 'accept_S6'),
        (guard__accept_S3__TO__accept_S7, 'accept_S7'),
        (guard__accept_S3__TO__accept_S8, 'accept_S8'),
        (guard__accept_S3__TO__accept_S9, 'accept_S9'),
        (guard__accept_S3__TO__accept_S10, 'accept_S10'),
        (guard__accept_S3__TO__accept_S11, 'accept_S11'),
        (guard__accept_S3__TO__accept_S12, 'accept_S12'),
        (guard__accept_S3__TO__accept_S13, 'accept_S13'),
        (guard__accept_S3__TO__accept_S14, 'accept_S14'),
        (guard__accept_S3__TO__accept_init, 'accept_init'),
        (guard__accept_S3__TO__accept_S15, 'accept_S15'),
        (guard__accept_S3__TO__accept_S16, 'accept_S16'),
    },
    'accept_S4' : {
        (guard__accept_S4__TO__accept_S2, 'accept_S2'),
        (guard__accept_S4__TO__accept_S3, 'accept_S3'),
        (guard__accept_S4__TO__accept_S4, 'accept_S4'),
        (guard__accept_S4__TO__accept_S5, 'accept_S5'),
        (guard__accept_S4__TO__accept_S6, 'accept_S6'),
        (guard__accept_S4__TO__accept_S7, 'accept_S7'),
        (guard__accept_S4__TO__accept_S8, 'accept_S8'),
        (guard__accept_S4__TO__accept_S9, 'accept_S9'),
        (guard__accept_S4__TO__accept_S10, 'accept_S10'),
        (guard__accept_S4__TO__accept_S11, 'accept_S11'),
        (guard__accept_S4__TO__accept_S12, 'accept_S12'),
        (guard__accept_S4__TO__accept_S13, 'accept_S13'),
        (guard__accept_S4__TO__accept_S14, 'accept_S14'),
        (guard__accept_S4__TO__accept_init, 'accept_init'),
        (guard__accept_S4__TO__accept_S15, 'accept_S15'),
        (guard__accept_S4__TO__accept_S16, 'accept_S16'),
    },
    'accept_S5' : {
        (guard__accept_S5__TO__accept_S2, 'accept_S2'),
        (guard__accept_S5__TO__accept_S3, 'accept_S3'),
        (guard__accept_S5__TO__accept_S4, 'accept_S4'),
        (guard__accept_S5__TO__accept_S5, 'accept_S5'),
        (guard__accept_S5__TO__accept_S6, 'accept_S6'),
        (guard__accept_S5__TO__accept_S7, 'accept_S7'),
        (guard__accept_S5__TO__accept_S8, 'accept_S8'),
        (guard__accept_S5__TO__accept_S9, 'accept_S9'),
        (guard__accept_S5__TO__accept_S10, 'accept_S10'),
        (guard__accept_S5__TO__accept_S11, 'accept_S11'),
        (guard__accept_S5__TO__accept_S12, 'accept_S12'),
        (guard__accept_S5__TO__accept_S13, 'accept_S13'),
        (guard__accept_S5__TO__accept_S14, 'accept_S14'),
        (guard__accept_S5__TO__accept_init, 'accept_init'),
        (guard__accept_S5__TO__accept_S15, 'accept_S15'),
        (guard__accept_S5__TO__accept_S16, 'accept_S16'),
    },
    'accept_S6' : {
        (guard__accept_S6__TO__accept_S2, 'accept_S2'),
        (guard__accept_S6__TO__accept_S3, 'accept_S3'),
        (guard__accept_S6__TO__accept_S4, 'accept_S4'),
        (guard__accept_S6__TO__accept_S5, 'accept_S5'),
        (guard__accept_S6__TO__accept_S6, 'accept_S6'),
        (guard__accept_S6__TO__accept_S7, 'accept_S7'),
        (guard__accept_S6__TO__accept_S8, 'accept_S8'),
        (guard__accept_S6__TO__accept_S9, 'accept_S9'),
        (guard__accept_S6__TO__accept_S10, 'accept_S10'),
        (guard__accept_S6__TO__accept_S11, 'accept_S11'),
        (guard__accept_S6__TO__accept_S12, 'accept_S12'),
        (guard__accept_S6__TO__accept_S13, 'accept_S13'),
        (guard__accept_S6__TO__accept_S14, 'accept_S14'),
        (guard__accept_S6__TO__accept_init, 'accept_init'),
        (guard__accept_S6__TO__accept_S15, 'accept_S15'),
        (guard__accept_S6__TO__accept_S16, 'accept_S16'),
    },
    'accept_S7' : {
        (guard__accept_S7__TO__accept_S2, 'accept_S2'),
        (guard__accept_S7__TO__accept_S3, 'accept_S3'),
        (guard__accept_S7__TO__accept_S4, 'accept_S4'),
        (guard__accept_S7__TO__accept_S5, 'accept_S5'),
        (guard__accept_S7__TO__accept_S6, 'accept_S6'),
        (guard__accept_S7__TO__accept_S7, 'accept_S7'),
        (guard__accept_S7__TO__accept_S8, 'accept_S8'),
        (guard__accept_S7__TO__accept_S9, 'accept_S9'),
        (guard__accept_S7__TO__accept_S10, 'accept_S10'),
        (guard__accept_S7__TO__accept_S11, 'accept_S11'),
        (guard__accept_S7__TO__accept_S12, 'accept_S12'),
        (guard__accept_S7__TO__accept_S13, 'accept_S13'),
        (guard__accept_S7__TO__accept_S14, 'accept_S14'),
        (guard__accept_S7__TO__accept_init, 'accept_init'),
        (guard__accept_S7__TO__accept_S15, 'accept_S15'),
        (guard__accept_S7__TO__accept_S16, 'accept_S16'),
    },
    'accept_S8' : {
        (guard__accept_S8__TO__accept_S2, 'accept_S2'),
        (guard__accept_S8__TO__accept_S3, 'accept_S3'),
        (guard__accept_S8__TO__accept_S4, 'accept_S4'),
        (guard__accept_S8__TO__accept_S5, 'accept_S5'),
        (guard__accept_S8__TO__accept_S6, 'accept_S6'),
        (guard__accept_S8__TO__accept_S7, 'accept_S7'),
        (guard__accept_S8__TO__accept_S8, 'accept_S8'),
        (guard__accept_S8__TO__accept_S9, 'accept_S9'),
        (guard__accept_S8__TO__accept_S10, 'accept_S10'),
        (guard__accept_S8__TO__accept_S11, 'accept_S11'),
        (guard__accept_S8__TO__accept_S12, 'accept_S12'),
        (guard__accept_S8__TO__accept_S13, 'accept_S13'),
        (guard__accept_S8__TO__accept_S14, 'accept_S14'),
        (guard__accept_S8__TO__accept_init, 'accept_init'),
        (guard__accept_S8__TO__accept_S15, 'accept_S15'),
        (guard__accept_S8__TO__accept_S16, 'accept_S16'),
    },
    'accept_S9' : {
        (guard__accept_S9__TO__accept_S2, 'accept_S2'),
        (guard__accept_S9__TO__accept_S3, 'accept_S3'),
        (guard__accept_S9__TO__accept_S4, 'accept_S4'),
        (guard__accept_S9__TO__accept_S5, 'accept_S5'),
        (guard__accept_S9__TO__accept_S6, 'accept_S6'),
        (guard__accept_S9__TO__accept_S7, 'accept_S7'),
        (guard__accept_S9__TO__accept_S8, 'accept_S8'),
        (guard__accept_S9__TO__accept_S9, 'accept_S9'),
        (guard__accept_S9__TO__accept_S10, 'accept_S10'),
        (guard__accept_S9__TO__accept_S11, 'accept_S11'),
        (guard__accept_S9__TO__accept_S12, 'accept_S12'),
        (guard__accept_S9__TO__accept_S13, 'accept_S13'),
        (guard__accept_S9__TO__accept_S14, 'accept_S14'),
        (guard__accept_S9__TO__accept_init, 'accept_init'),
        (guard__accept_S9__TO__accept_S15, 'accept_S15'),
        (guard__accept_S9__TO__accept_S16, 'accept_S16'),
    },
    'accept_S10' : {
        (guard__accept_S10__TO__accept_S2, 'accept_S2'),
        (guard__accept_S10__TO__accept_S3, 'accept_S3'),
        (guard__accept_S10__TO__accept_S4, 'accept_S4'),
        (guard__accept_S10__TO__accept_S5, 'accept_S5'),
        (guard__accept_S10__TO__accept_S6, 'accept_S6'),
        (guard__accept_S10__TO__accept_S7, 'accept_S7'),
        (guard__accept_S10__TO__accept_S8, 'accept_S8'),
        (guard__accept_S10__TO__accept_S9, 'accept_S9'),
        (guard__accept_S10__TO__accept_S10, 'accept_S10'),
        (guard__accept_S10__TO__accept_S11, 'accept_S11'),
        (guard__accept_S10__TO__accept_S12, 'accept_S12'),
        (guard__accept_S10__TO__accept_S13, 'accept_S13'),
        (guard__accept_S10__TO__accept_S14, 'accept_S14'),
        (guard__accept_S10__TO__accept_init, 'accept_init'),
        (guard__accept_S10__TO__accept_S15, 'accept_S15'),
        (guard__accept_S10__TO__accept_S16, 'accept_S16'),
    },
    'accept_S11' : {
        (guard__accept_S11__TO__accept_S2, 'accept_S2'),
        (guard__accept_S11__TO__accept_S3, 'accept_S3'),
        (guard__accept_S11__TO__accept_S4, 'accept_S4'),
        (guard__accept_S11__TO__accept_S5, 'accept_S5'),
        (guard__accept_S11__TO__accept_S6, 'accept_S6'),
        (guard__accept_S11__TO__accept_S7, 'accept_S7'),
        (guard__accept_S11__TO__accept_S8, 'accept_S8'),
        (guard__accept_S11__TO__accept_S9, 'accept_S9'),
        (guard__accept_S11__TO__accept_S10, 'accept_S10'),
        (guard__accept_S11__TO__accept_S11, 'accept_S11'),
        (guard__accept_S11__TO__accept_S12, 'accept_S12'),
        (guard__accept_S11__TO__accept_S13, 'accept_S13'),
        (guard__accept_S11__TO__accept_S14, 'accept_S14'),
        (guard__accept_S11__TO__accept_init, 'accept_init'),
        (guard__accept_S11__TO__accept_S15, 'accept_S15'),
        (guard__accept_S11__TO__accept_S16, 'accept_S16'),
    },
    'accept_S12' : {
        (guard__accept_S12__TO__accept_S2, 'accept_S2'),
        (guard__accept_S12__TO__accept_S3, 'accept_S3'),
        (guard__accept_S12__TO__accept_S4, 'accept_S4'),
        (guard__accept_S12__TO__accept_S5, 'accept_S5'),
        (guard__accept_S12__TO__accept_S6, 'accept_S6'),
        (guard__accept_S12__TO__accept_S7, 'accept_S7'),
        (guard__accept_S12__TO__accept_S8, 'accept_S8'),
        (guard__accept_S12__TO__accept_S9, 'accept_S9'),
        (guard__accept_S12__TO__accept_S10, 'accept_S10'),
        (guard__accept_S12__TO__accept_S11, 'accept_S11'),
        (guard__accept_S12__TO__accept_S12, 'accept_S12'),
        (guard__accept_S12__TO__accept_S13, 'accept_S13'),
        (guard__accept_S12__TO__accept_S14, 'accept_S14'),
        (guard__accept_S12__TO__accept_init, 'accept_init'),
        (guard__accept_S12__TO__accept_S15, 'accept_S15'),
        (guard__accept_S12__TO__accept_S16, 'accept_S16'),
    },
    'accept_S13' : {
        (guard__accept_S13__TO__accept_S2, 'accept_S2'),
        (guard__accept_S13__TO__accept_S3, 'accept_S3'),
        (guard__accept_S13__TO__accept_S4, 'accept_S4'),
        (guard__accept_S13__TO__accept_S5, 'accept_S5'),
        (guard__accept_S13__TO__accept_S6, 'accept_S6'),
        (guard__accept_S13__TO__accept_S7, 'accept_S7'),
        (guard__accept_S13__TO__accept_S8, 'accept_S8'),
        (guard__accept_S13__TO__accept_S9, 'accept_S9'),
        (guard__accept_S13__TO__accept_S10, 'accept_S10'),
        (guard__accept_S13__TO__accept_S11, 'accept_S11'),
        (guard__accept_S13__TO__accept_S12, 'accept_S12'),
        (guard__accept_S13__TO__accept_S13, 'accept_S13'),
        (guard__accept_S13__TO__accept_S14, 'accept_S14'),
        (guard__accept_S13__TO__accept_init, 'accept_init'),
        (guard__accept_S13__TO__accept_S15, 'accept_S15'),
        (guard__accept_S13__TO__accept_S16, 'accept_S16'),
    },
    'accept_S14' : {
        (guard__accept_S14__TO__accept_S2, 'accept_S2'),
        (guard__accept_S14__TO__accept_S3, 'accept_S3'),
        (guard__accept_S14__TO__accept_S4, 'accept_S4'),
        (guard__accept_S14__TO__accept_S5, 'accept_S5'),
        (guard__accept_S14__TO__accept_S6, 'accept_S6'),
        (guard__accept_S14__TO__accept_S7, 'accept_S7'),
        (guard__accept_S14__TO__accept_S8, 'accept_S8'),
        (guard__accept_S14__TO__accept_S9, 'accept_S9'),
        (guard__accept_S14__TO__accept_S10, 'accept_S10'),
        (guard__accept_S14__TO__accept_S11, 'accept_S11'),
        (guard__accept_S14__TO__accept_S12, 'accept_S12'),
        (guard__accept_S14__TO__accept_S13, 'accept_S13'),
        (guard__accept_S14__TO__accept_S14, 'accept_S14'),
        (guard__accept_S14__TO__accept_init, 'accept_init'),
        (guard__accept_S14__TO__accept_S15, 'accept_S15'),
        (guard__accept_S14__TO__accept_S16, 'accept_S16'),
    },
    'accept_S15' : {
        (guard__accept_S15__TO__accept_S2, 'accept_S2'),
        (guard__accept_S15__TO__accept_S3, 'accept_S3'),
        (guard__accept_S15__TO__accept_S4, 'accept_S4'),
        (guard__accept_S15__TO__accept_S5, 'accept_S5'),
        (guard__accept_S15__TO__accept_S6, 'accept_S6'),
        (guard__accept_S15__TO__accept_S7, 'accept_S7'),
        (guard__accept_S15__TO__accept_S8, 'accept_S8'),
        (guard__accept_S15__TO__accept_S9, 'accept_S9'),
        (guard__accept_S15__TO__accept_S10, 'accept_S10'),
        (guard__accept_S15__TO__accept_S11, 'accept_S11'),
        (guard__accept_S15__TO__accept_S12, 'accept_S12'),
        (guard__accept_S15__TO__accept_S13, 'accept_S13'),
        (guard__accept_S15__TO__accept_S14, 'accept_S14'),
        (guard__accept_S15__TO__accept_init, 'accept_init'),
        (guard__accept_S15__TO__accept_S15, 'accept_S15'),
        (guard__accept_S15__TO__accept_S16, 'accept_S16'),
    },
    'accept_S16' : {
        (guard__accept_S16__TO__accept_S2, 'accept_S2'),
        (guard__accept_S16__TO__accept_S3, 'accept_S3'),
        (guard__accept_S16__TO__accept_S4, 'accept_S4'),
        (guard__accept_S16__TO__accept_S5, 'accept_S5'),
        (guard__accept_S16__TO__accept_S6, 'accept_S6'),
        (guard__accept_S16__TO__accept_S7, 'accept_S7'),
        (guard__accept_S16__TO__accept_S8, 'accept_S8'),
        (guard__accept_S16__TO__accept_S9, 'accept_S9'),
        (guard__accept_S16__TO__accept_S10, 'accept_S10'),
        (guard__accept_S16__TO__accept_S11, 'accept_S11'),
        (guard__accept_S16__TO__accept_S12, 'accept_S12'),
        (guard__accept_S16__TO__accept_S13, 'accept_S13'),
        (guard__accept_S16__TO__accept_S14, 'accept_S14'),
        (guard__accept_S16__TO__accept_init, 'accept_init'),
        (guard__accept_S16__TO__accept_S15, 'accept_S15'),
        (guard__accept_S16__TO__accept_S16, 'accept_S16'),
    },
}
INITIAL_STATE = 'accept_init'
ACCEPTING_STATE = None
SAFE = 'safe'
UNSAFE = 'unsafe'
UNKNOWN = 'unknown'
def p0_func(model_state):
    return (model_state['current_action'] == 'left')
def p1_func(model_state):
    return (model_state['current_action'] != 'right')
def p2_func(model_state):
    return (model_state['current_action'] == 'right')
def p3_func(model_state):
    return (model_state['current_action'] != 'left')
def p4_func(model_state):
    return (model_state['current_action'] == 'up')
def p5_func(model_state):
    return (model_state['current_action'] != 'down')
def p6_func(model_state):
    return (model_state['current_action'] == 'down')
def p7_func(model_state):
    return (model_state['current_action'] != 'up')
MODEL_INFO_FUNCTIONS = {
    'p0' : p0_func,
    'p1' : p1_func,
    'p2' : p2_func,
    'p3' : p3_func,
    'p4' : p4_func,
    'p5' : p5_func,
    'p6' : p6_func,
    'p7' : p7_func,
}
def model_state_to_model_info(model_state):
    return {
        key : item(model_state)
        for (key, item) in MODEL_INFO_FUNCTIONS.items()
    }

def transition(automaton_states, model_state):
    if ACCEPTING_STATE is not None and ACCEPTING_STATE in automaton_states:
        return ({ACCEPTING_STATE}, SAFE)
    if len(automaton_states) == 0:
        return (set(), UNSAFE)
    model_info = model_state_to_model_info(model_state)
    new_automaton_states = {
        new_automaton_state
        for automaton_state in automaton_states
        for (guard, new_automaton_state) in STATE_TRANS[automaton_state]
        if guard(model_info)
    }
    if ACCEPTING_STATE is not None and ACCEPTING_STATE in new_automaton_states:
        return ({ACCEPTING_STATE}, SAFE)
    if len(new_automaton_states) == 0:
        return (set(), UNSAFE)
    return (new_automaton_states, UNKNOWN)

import random
def test_loop(max_iter):
    current_states = {INITIAL_STATE}
    rb = ('left', 'right', 'up', 'down', 'no_action')
    for count in range(max_iter):
        model_state = {
            'current_action' : random.choice(rb)
        }
        (current_states, status) = transition(current_states, model_state)
        print('--------------------' + str(count))
        print(model_state)
        print(current_states)
        print(status)
        if status != UNKNOWN:
            print('RESETTING')
            current_states = {INITIAL_STATE}
    return

if __name__ == '__main__':
    test_loop(20)
