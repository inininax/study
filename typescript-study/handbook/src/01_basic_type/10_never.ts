const error = (message: string): never => {
    throw new Error(message);
}

const fail = () => {
    return error('Something failed');
};

const infiniteLoop = () => {
    while (true) {
    }
};