





def merge_test_matrices_and_phys_data(matrices, phys_data):
    merged_dfs = []
    for M in matrices:
        merged = phys_data.merge(
            M, on=["X", "Y", "Month"], how="inner"
        )
    return merged_dfs