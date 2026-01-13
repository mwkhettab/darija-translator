<script lang="ts">
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import * as messages from '$lib/paraglide/messages';

	const status = page.status;
	const isNotFound = status === 404;

	const copy = {
		title: isNotFound
			? messages['error.404.title']()
			: messages['error.unexpected.title'](),
		message: isNotFound
			? messages['error.404.message']()
			: messages['error.unexpected.message'](),
		homeLink: messages['error.home']()
	};
</script>

<svelte:head>
	<title>{copy.title}</title>
	<meta name="robots" content="noindex" />
</svelte:head>

<section class="error">
	<div class="error-content">
		<h1 class="error-title">{status}</h1>
		<h2 class="error-subtitle">{copy.title}</h2>
		<p class="error-message">{copy.message}</p>
		<a href={resolve('/')} class="error-home-link">
			{copy.homeLink}
		</a>
	</div>
</section>

<style>
	.error {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 90vh;
		padding: 20px;
		text-align: center;
		color: white;
		background: var(--moroccan-red);
	}

	.error-content {
		max-width: 600px;
		padding: 40px;
		border-radius: 10px;
		background-color: white;
		color: black;
		border-top: 8px solid var(--moroccan-green);
	}

	.error-title {
		margin: 0;
		font-size: 6rem;
		color: var(--moroccan-red);
	}

	.error-subtitle {
		margin: 10px 0;
		font-size: 2rem;
	}

	.error-message {
		margin: 20px 0;
		font-size: 1.2rem;
	}

	.error-home-link {
		display: inline-block;
		margin-top: 20px;
		padding: 10px 20px;
		border-radius: 5px;
		background-color: var(--moroccan-green);
		color: white;
		text-decoration: none;
		transition: background-color 0.3s ease;
	}

	.error-home-link:hover {
		background-color: #004d1a;
	}
</style>
