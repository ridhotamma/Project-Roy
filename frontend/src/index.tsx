import { render } from 'preact';
import { LocationProvider, Router, Route } from 'preact-iso';

import { Header } from './components/Header.jsx';
import { Home } from './pages/Home/index.jsx';
import { Login } from './pages/Login/index.js';
import { NotFound } from './pages/_404.jsx';
import './index.css';

export function App() {
	return (
		<LocationProvider>
			<Header />
			<main class="bg-white">
				<Router>
					<Route path="/login" component={Login} />
					<Route path="/" component={Home} />
					<Route default component={NotFound} />
				</Router>
			</main>
		</LocationProvider>
	);
}

render(<App />, document.getElementById('app'));
