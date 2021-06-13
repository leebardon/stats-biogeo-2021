import numpy as np

def random_test_matrices(SEEDS):
    num_cells = [
        100,
        200,
        400,
        600,
        800,
        1000,
        1500,
        2000,
        3000,
        4000,
        5000,
        6000,
        8000,
        10000,
        12000,
        14000,
        16000,
        18000,
    ]
    matrices = []
    for seed in SEEDS:
        for N in num_cells:
            Ir = np.zeros(shape=(144, 90, 265))
            rng = np.random.default_rng(seed)
            for _ in range(N):
                rx = rng.integers(low=0, high=144)
                ry = rng.integers(low=0, high=90)
                rt = rng.integers(low=0, high=264)
                Ir[rx, ry, rt] = 1
            matrices.append(Ir)
    return matrices, num_cells