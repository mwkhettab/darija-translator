<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import type { Pathname } from '$app/types';

	import morocco from '$lib/images/morocco-map.png';
	import * as messages from '$lib/paraglide/messages';

	import MenuIcon from 'virtual:icons/mdi/menu';
	import CloseIcon from 'virtual:icons/mdi/close';

	import { fade } from 'svelte/transition';

	let isMenuOpen = $state(false);

	const navLinks = [
		{ href: '/' as Pathname, label: messages['nav.home']() },
		{ href: '/about' as Pathname, label: messages['nav.about']() },
		{ href: '/translate' as Pathname, label: messages['nav.translate']() }
	];

	const isActive = (href: string) => page.url.pathname === href;

	const toggleMenu = () => {
		isMenuOpen = !isMenuOpen;
	};

	const closeMenu = () => {
		isMenuOpen = false;
	};

	$effect(() => {
		const originalOverflow = document.body.style.overflow;

		document.body.style.overflow = isMenuOpen ? 'hidden' : originalOverflow;

		return () => {
			document.body.style.overflow = originalOverflow;
		};
	});
</script>

<header>
	<!-- DESKTOP -->
	<div class="header-desktop">
		<div class="container">
			<div class="logo">
				<a href={resolve('/')}>
					<img src={morocco} alt="Morocco Map" width="50" height="50" draggable="false" />
					<h1>{messages.header()}</h1>
				</a>
			</div>

			<nav class="links">
				{#each navLinks as link (link.href)}
					<a href={resolve(link.href)} class={isActive(link.href) ? 'active' : undefined}>
						{link.label}
					</a>
				{/each}
			</nav>
		</div>
	</div>

	<!-- MOBILE HEADER -->
	<div class="header-mobile">
		<div class="logo">
			<a href={resolve('/')}>
				<img src={morocco} alt="Morocco Map" width="40" height="40" />
				<h1>{messages.header()}</h1>
			</a>
		</div>

		<button type="button" class="menu-button" aria-label="Toggle menu" onclick={toggleMenu}>
			<MenuIcon width="24" height="24" />
		</button>
	</div>

	<!-- MOBILE MENU -->
	{#if isMenuOpen}
		<nav class="mobile-menu" in:fade={{ duration: 200 }} out:fade={{ duration: 150 }}>
			<button class="close-button" aria-label="Close menu" onclick={closeMenu}>
				<CloseIcon width="28" height="28" />
			</button>

			{#each navLinks as link (link.href)}
				<a
					href={resolve(link.href)}
					class={isActive(link.href) ? 'active' : undefined}
					onclick={closeMenu}
				>
					{link.label}
				</a>
			{/each}
		</nav>
	{/if}
</header>

<style>
	/* DESKTOP STYLES */
	.header-desktop {
		display: none;
		width: 100%;
		min-height: 10vh;
	}

	.container {
		max-width: 960px;
		margin: 0 auto;
		padding: 10px 20px;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.links a {
		position: relative;
		margin-left: 20px;
		font-weight: bold;
		text-decoration: none;
		padding: 6px 0;
		transition:
			color 0.2s ease,
			transform 0.15s ease;
	}

	.links a::after {
		content: '';
		position: absolute;
		left: 0;
		bottom: -2px;
		width: 100%;
		height: 2px;
		background: currentColor;
		transform: scaleX(0);
		transform-origin: left;
		transition: transform 0.2s ease;
	}

	.links a:hover {
		transform: translateY(-1px);
	}

	.links a:hover::after {
		transform: scaleX(1);
	}

	.links a:focus-visible {
		outline: none;
	}

	.links a:focus-visible::after {
		transform: scaleX(1);
	}

	.links a.active::after {
		transform: scaleX(1);
	}

	.logo a {
		display: flex;
		align-items: center;
		white-space: nowrap;
		gap: 16px;
	}

	/* MOBILE STYLES */
	.header-mobile {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 10px 16px;
		gap: 12px;
		min-height: 10vh;
	}

	.header-mobile .logo {
		flex: 1;
		min-width: 0;
	}

	.header-mobile .logo h1 {
		font-size: clamp(1rem, 4vw, 1.25rem);
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.menu-button {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-shrink: 0;
		width: 48px;
		height: 40px;
		padding: 0;
		border: none;
		cursor: pointer;
	}

	.menu-button:hover {
		background-color: var(--moroccan-red);
		transform: none;
	}

	.mobile-menu {
		position: fixed;
		inset: 0;
		width: 100vw;
		height: 100dvh;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: 24px;

		background-color: var(--moroccan-red);
		z-index: 1000;
	}

	.mobile-menu a {
		color: white;
		font-size: 1.5rem;
		font-weight: bold;
		text-decoration: none;
		transition: transform 0.15s ease;
		position: relative;
		padding-bottom: 4px;
	}

	.mobile-menu a.active::after {
		content: '';
		position: absolute;
		left: 0;
		bottom: 0;
		width: 100%;
		height: 3px;
		background: white;
	}

	@media (min-width: 670px) {
		.header-desktop {
			display: block;
		}

		.header-mobile,
		.mobile-menu {
			display: none;
		}
	}

	.close-button {
		position: absolute;
		top: 16px;
		right: 16px;

		background: none;
		border: none;

		width: 44px;
		height: 44px;

		cursor: pointer;
	}
</style>
