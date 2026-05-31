import React from 'react';
import ContextProvider from './context/ContextProvider';
import StoreProvider from './redux/StoreProvider';
import Middleware from './redux/Middleware';

export default function App() {
	return (
		<div>
			<ContextProvider />
			<hr />
			<StoreProvider />
			<Middleware />
		</div>
	);
};
