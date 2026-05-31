// union type
declare function create(o: object | null): void;

create({prop: 0});
create(null);
// create(52); (X)
// create('string'); (X)
// create(false); (X)
// create(undefined); (X)