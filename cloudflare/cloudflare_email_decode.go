package main

import (
    "bytes"
    "strconv"
)

func cf(a string) (s string) {
    var e bytes.Buffer
    r, _ := strconv.ParseInt(a[0:2], 16, 0)
    for n := 4; n < len(a)+2; n += 2 {
        i, _ := strconv.ParseInt(a[n-2:n], 16, 0)
        e.WriteString(string(i ^ r))
    }
    return e.String()
}

func main() {
    email := cf("9ef4fffdf5e7ebdee4fbebedfbfbb0fdf1f3")
    print(email)
    print("\n")
}
