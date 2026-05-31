// reset parameters
function resetParam(firstName: string, ...resetOfName: string[]) {
    return firstName + ' ' + resetOfName.join(' ');
}

let resetParamFun: (firstName: string, ...resetOfName: string[]) => string = resetParam;

resetParam('Joseph', 'Samuel', 'Lucas', 'MacKinzie');
resetParamFun('Joseph', 'Samuel', 'Lucas', 'MacKinzie');