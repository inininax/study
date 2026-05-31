import { applyMiddleware, createStore } from '@reduxjs/toolkit';

const myMiddleware = (store: any) => (next: any) => (action: any) => next(action);
const middleware1 = (store: any) => (next: any) => (action: any) => {
	console.log('middleware1 start');
	const result = next(action);
	console.log('middleware1 end');
	return result;
};
const middleware2 = (store: any) => (next: any) => (action: any) => {
	console.log('middleware2 start');
	const result = next(action);
	console.log('middleware2 end');
	return result;
};
const myReducer = (state: any, action: any) => {
	console.log('myReducer');
	return state;
};
const store = createStore(myReducer, applyMiddleware(middleware1, middleware2));
store.dispatch({ type: 'someAction' });

export default function Middleware() {
	return (
		<div>Middleware</div>
	);
}