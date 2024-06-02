import { render } from 'preact';
import { LocationProvider, Router, Route } from 'preact-iso';

import { Header } from './components/Header';
import { Home } from './pages/Home/index';
import { Login } from './pages/Login/index';
import { NotFound } from './pages/_404';
import './index.css';

export function App() {
	return (
		<LocationProvider>
			<Header />
			<main>
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
