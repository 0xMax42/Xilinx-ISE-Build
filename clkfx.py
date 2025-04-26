def find_best_clkfx(input_freq, target_freq):
    best_m = 0
    best_d = 0
    best_error = float('inf')
    best_output = 0

    for m in range(2, 33):  # CLKFX_MULTIPLY 2..32
        for d in range(1, 33):  # CLKFX_DIVIDE 1..32
            output_freq = input_freq * m / d
            error = abs(output_freq - target_freq)

            if error < best_error:
                best_error = error
                best_m = m
                best_d = d
                best_output = output_freq

    relative_error = (best_error / target_freq) * 100

    print(f"Beste Werte:")
    print(f"  CLKFX_MULTIPLY => {best_m}")
    print(f"  CLKFX_DIVIDE   => {best_d}")
    print(f"Erzeugte Frequenz: {best_output:.6f} MHz")
    print(f"Abweichung: {best_error:.6f} MHz ({relative_error:.3f}%)")

if __name__ == "__main__":
    input_freq = float(input("Eingangsfrequenz (MHz): "))
    target_freq = float(input("Ziel-Frequenz (MHz): "))
    find_best_clkfx(input_freq, target_freq)
