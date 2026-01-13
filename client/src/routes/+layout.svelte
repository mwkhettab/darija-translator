<script lang="ts">
	import { page } from '$app/state';
	import { getLocale, setLocale } from '$lib/paraglide/runtime';
	import * as messages from '$lib/paraglide/messages';

	import Header from '$lib/layout/Header.svelte';
	import Footer from '$lib/layout/Footer.svelte';

	import './layout.css';

	let { children } = $props();

	type Locale = 'en' | 'fr' | 'ar';

	$effect(() => {
		const pathLocale = page.url.pathname.split('/')[1];

		if (pathLocale !== 'en' && pathLocale !== 'fr' && pathLocale !== 'ar') {
			return;
		}

		setLocale(pathLocale as Locale);
	});

	const isArabic = $derived(getLocale() === 'ar');

	const metaTitle = messages['meta.title']();
	const metaDescription = messages['meta.description']();
</script>

<svelte:head>
	<title>{metaTitle}</title>
	<meta name="description" content={metaDescription} />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<div class={isArabic ? 'ar' : undefined}>
	<Header />
	<main>{@render children()}</main>
	<Footer />
</div>
