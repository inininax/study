export {};

// type 제한
function identity<T extends number | string>(p1: T): T {
    return p1;
}

identity(1);
identity('a');
// identity([]); // error