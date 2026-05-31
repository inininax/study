import { createStore } from '@reduxjs/toolkit';
import { Provider, useDispatch, useSelector } from 'react-redux';

interface StoreType {
	user: { name: string },
	product: { name: string }
}

const INITIAL_STATE: StoreType = {
	user: { name: 'store mike' },
	product: { name: 'store iphone' },
};

function reducer(state: StoreType = INITIAL_STATE, action: any): StoreType {
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

const store = createStore(reducer);

export default function StoreProvider() {
	return (
		<div>
			<Provider store={store}>
				<User />
				<Product />
			</Provider>
		</div>
	);
};

function User() {
	console.log('User render2');
	const user = useSelector((state: StoreType) => state.user);
	const dispatch = useDispatch();
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
	console.log('Product render2');
	const product = useSelector((state: StoreType) => state.product);
	return (
		<p>
			{`제품 이름: ${product.name}`}
		</p>
	);
}