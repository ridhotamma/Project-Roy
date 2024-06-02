import { useLocation } from 'preact-iso';

export function Header() {
	const { url } = useLocation();

	return (
		<header class="sticky top-0 p-4 bg-blue-600 text-white">
			<nav class="flex justify-end items-center gap-4">
				<a href="/" class={url == '/' && 'active'}>
					Home
				</a>
				<a href="/login" class={url == '/login' && 'active'}>
					Login
				</a>
			</nav>
		</header>
	);
}
