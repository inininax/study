# React Redux
```shell
yarn add react-redux
yarn add @types/react-redux
```

- 단방향 흐름
```text
- 액션 > 미들웨어 > 리듀서 > 스토어 > 뷰 > 액션
```

- 액션 (type 속성 값은 유니크)
```javascript
export const ADD = 'todo/ADD';
export const REMOVE = 'todo/REMOVE';
export const REMOVE_ALL = 'todo/REMOVE_ALL';

export function addTodo({ title, priority }) {
	return { type: ADD, title, priority };
}
export function removeTodo({ id }) {
	return { type: REMOVE, id };
}
export function removeAllTodo() {
	return { type: REMOVE_ALL };
}

// store.dispatch(addTodo({title:'', priority: 1}));
// store.dispatch(removeTodo(1));
// store.dispatch(removeAllTodo());
```

- 미들웨어
```javascript
const myMiddleware = store => next => action => next(action);
const middleware1 = store => next => action => {
	console.log('middleware1 start');
	const result = next(action);
	console.log('middleware1 end');
	return result;
};
const middleware2 = store => next => action => {
	console.log('middleware2 start');
	const result = next(action);
	console.log('middleware2 end');
	return result;
};
const myReducer = (state, action) => {
	console.log('myReducer');
	return state;
}
const store = createStore(myReducer, applyMiddleware(middleware1, middleware2));
store.dispatch({ type: 'someAction' });
```
