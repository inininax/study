// Optional and Default Parameter
function buildName(firstName: string, lastName: string) {
    return firstName = " " + lastName;
}

function buildName2(firstName: string, lastName: string = 'Smith') {
    return firstName + ' ' + lastName;
}

function buildName3(firstName: string, lastName?: string) {
    return firstName + ' ' + lastName;
}

// buildName('Bob'); // Optional and Default Parameter
// buildName('Bob', 'Adams', 'Sr.'); // Optional and Default Paramete
buildName('Bob', 'Adams');

buildName2('Bob');
buildName2('Bob', undefined);
buildName2('Bob', 'Adams');
// buildName2('Bob', 'Adams', 'Sr.');

buildName3('Bob');
buildName3('Bob', undefined);
buildName3('Bob', 'Adams');
