from src.mechanics import calculate

if __name__ == "__main__":
    result = calculate(span=[45, ] * 4, dForce=[[a for a in range(181)], ], moment_loc=[45])
    print(result)
    f = 1
