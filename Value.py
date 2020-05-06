def state_value(grid, knocked, turn):

    if turn <= 10:

        weightgrid =[          [0,0,0,0,0,0],
                              [0,1,1,1,1,1,0],
                             [0,1,2,2,2,2,1,0],
                            [0,1,2,3,3,3,2,1,0],
                           [0,1,2,3,4,4,3,2,1,0],
                          [0,1,2,3,4,5,4,3,2,1,0],
                           [0,1,2,3,4,4,3,2,1,0],
                            [0,1,2,3,3,3,2,1,0],
                             [0,3,2,2,2,2,1,0],
                              [0,3,1,1,1,1,0],
                               [0,0,0,0,0,0]
                                                    ]

    else:

        weightgrid =[      [0,0,0,0,0,0],
                          [0,3,3,3,3,3,0],
                         [0,3,3,3,3,3,3,0],
                        [0,3,3,2,2,2,3,3,0],
                       [0,3,3,2,1,1,2,3,3,0],
                      [0,3,3,2,1,1,1,2,3,3,0],
                       [0,3,3,2,1,1,2,3,3,0],
                        [0,3,3,2,2,2,3,3,0],
                         [0,3,3,3,3,3,3,0],
                          [0,3,3,3,3,3,0],
                           [0,0,0,0,0,0]
                                                ]

    value = 0

    if knocked == 1:
        value = -1000
        return value
    elif knocked == 2:
        value = 1000
        return value
    else:

        for i in range(1,10):
            for j in range(1, len(weightgrid[i]) - 1):
                if grid[i][j] == 1:
                    value += weightgrid[i][j]
                if grid[i][j] == 2:
                    value -= weightgrid[i][j]
        return value
