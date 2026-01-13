<script lang="ts">
	import { resolve } from '$app/paths';
	import type { Pathname } from '$app/types';

	import morocco from '$lib/images/morocco2.jpeg';
	import * as m from '$lib/paraglide/messages';

	const about = {
		title: m['about.title'](),
		paragraphs: [m['about.paragraph1'](), m['about.paragraph4'](), m['about.paragraph5']()],
		highlighted: {
			before: m['about.paragraph2'](),
			highlight: m['about.highlight'](),
			after: m['about.paragraph3']()
		},
		signature: m['about.signature']()
	};

	const actions = {
		primary: {
			href: '/translate' as Pathname,
			label: m['cta.button']()
		},
		secondary: {
			href: '/' as Pathname,
			label: m['nav.home']()
		}
	};
</script>

<section class="about" style="--bg: url('{morocco}')">
	<div class="about-overlay"></div>

	<div class="about-content">
		<h1>{about.title}</h1>

		<div class="about-text">
			<p>{about.paragraphs[0]}</p>

			<p>
				{about.highlighted.before}
				<strong>{about.highlighted.highlight}</strong>.
				{about.highlighted.after}
			</p>

			<p>{about.paragraphs[1]}</p>
			<p>{about.paragraphs[2]}</p>

			<p class="signature">{about.signature}</p>
		</div>

		<div class="about-actions">
			<a href={resolve(actions.primary.href)} class="about-btn primary">
				{actions.primary.label}
			</a>

			<a href={resolve(actions.secondary.href)} class="about-btn secondary">
				{actions.secondary.label}
			</a>
		</div>
	</div>
</section>

<style>
	.about {
		position: relative;
		width: 100%;
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 3rem 1.5rem;
		box-sizing: border-box;
		overflow: hidden;
	}

	.about::before {
		content: '';
		position: absolute;
		inset: 0;
		background-image: var(--bg);
		background-size: cover;
		background-position: center;
		filter: blur(4px);
		transform: scale(1.1);
		z-index: 0;
	}

	.about-overlay {
		position: absolute;
		inset: 0;
		background: rgba(0, 0, 0, 0.55);
		z-index: 1;
	}

	.about-content {
		position: relative;
		z-index: 2;
		max-width: 800px;
		background: rgba(255, 255, 255, 0.98);
		padding: 3rem 2.5rem;
		border-radius: 20px;
		box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
		border-top: 8px solid var(--moroccan-red);
	}

	.about-content h1 {
		color: var(--moroccan-red);
		text-align: center;
		margin: 0 0 2rem;
		font-size: 2.5rem;
	}

	.about-text {
		color: #333;
		line-height: 1.8;
		font-size: 1.1rem;
	}

	.about-text p {
		margin-bottom: 1.5rem;
	}

	.about-text strong {
		color: var(--moroccan-red);
		font-weight: 600;
	}

	.signature {
		font-style: italic;
		color: var(--moroccan-green);
		font-weight: 600;
		text-align: center;
		margin-top: 2rem;
		font-size: 1.15rem;
	}

	.about-actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
		margin-top: 2.5rem;
	}

	.about-btn {
		display: inline-block;
		padding: 0.85rem 2.5rem;
		border-radius: 10px;
		font-weight: 600;
		text-decoration: none;
		transition:
			transform 0.2s ease,
			background-color 0.3s ease,
			color 0.3s ease,
			box-shadow 0.2s ease;
	}

	.about-btn.primary {
		background: var(--moroccan-red);
		color: white;
		box-shadow: 0 4px 15px rgba(201, 23, 23, 0.3);
	}

	.about-btn.primary:hover {
		background: var(--moroccan-green);
		transform: translateY(-2px);
		box-shadow: 0 6px 20px rgba(21, 128, 61, 0.4);
	}

	.about-btn.secondary {
		border: 2px solid var(--moroccan-green);
		color: var(--moroccan-green);
		background: white;
	}

	.about-btn.secondary:hover {
		background: var(--moroccan-green);
		color: white;
		transform: translateY(-2px);
		box-shadow: 0 6px 20px rgba(21, 128, 61, 0.3);
	}

	@media (max-width: 768px) {
		.about-content {
			padding: 2rem 1.5rem;
		}

		.about-content h1 {
			font-size: 2rem;
		}

		.about-text {
			font-size: 1rem;
		}

		.about-btn {
			padding: 0.75rem 2rem;
		}
	}
</style>
