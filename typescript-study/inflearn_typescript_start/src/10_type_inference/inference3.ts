export {};

const arr1 = [10, 20, 30];
const [n1, n2, n3] = arr1; // 비구조화 할당 , destructuring
// arr1.push('a'); // error

const obj = {id: 'abc', age: 123, language: 'korean'};
const {id, age, language} = obj;

// console.log( id === age ); // error