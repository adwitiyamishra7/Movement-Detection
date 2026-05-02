"""Demo showing `//` comments supported via the pycpp runner or import hook."""

def main():
    # start-of-line comment — will be ignored
    // this is a C++ style comment
    print("This prints; // comment above ignored")

    # floor-division should still work under default mode
    x = 10 // 3
    print("10 // 3 =", x)

    text = "string with // inside stays intact"
    print(text)


if __name__ == "__main__":
    main()
