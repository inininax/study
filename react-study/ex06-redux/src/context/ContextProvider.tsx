import { createContext, useContext, useReducer } from 'react';

const INITIAL_STATE = {
	user: { name: 'mike' },
	product: { name: 'iphone' },
};
const AppContext = createContext(INITIAL_STATE);
const DispatchContext = createContext((value: any) => {
});

function reducer(state: any, action: any) {
	switch (action.type) {
		case 'setUserName':
			return {
				...state,
				user: { ...state.user, name: action.name },
			};
		default:
			return state;
	}
}

export default function ContextProvider() {
	const [state, dispatch] = useReducer(reducer, INITIAL_STATE);
	return (
		<div>
			<AppContext.Provider value={state}>
				<DispatchContext.Provider value={dispatch}>
					<User />
					<Product />
				</DispatchContext.Provider>
			</AppContext.Provider>
		</div>
	);
};

function User() {
	console.log('User render');
	const { user } = useContext(AppContext);
	const dispatch = useContext(DispatchContext);
	return (
		<div>
			<p>{`${user.name}님 안녕하세요.`}</p>
			<button onClick={() => dispatch({ type: 'setUserName', name: 'john' })}>
				사용자 이름 수정
			</button>
		</div>
	);
}

function Product() {
	console.log('Product render');
	const { product } = useContext(AppContext);
	return (
		<p>
			{`제품 이름: ${product.name}`}
		</p>
	);
}