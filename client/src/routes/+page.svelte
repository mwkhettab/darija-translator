<script lang="ts">
	import morocco from '$lib/images/morocco.png';
	import * as m from '$lib/paraglide/messages';
	import { resolve } from '$app/paths';

	const hero = {
		title: m['hero.title'](),
		text: m['hero.text'](),
		ctaPrimary: m['hero.cta.primary'](),
		ctaSecondary: m['hero.cta.secondary']()
	};

	const value = {
		title: m['value.title'](),
		items: [
			{
				title: m['value.accuracy.title'](),
				text: m['value.accuracy.text']()
			},
			{
				title: m['value.usability.title'](),
				text: m['value.usability.text']()
			},
			{
				title: m['value.free.title'](),
				text: m['value.free.text']()
			}
		]
	};

	const examples = {
		title: m['examples.title'](),
		subtitle: m['examples.subtitle'](),
		darija: m['darija'](),
		list: [
			{
				enLabel: m['examples.example1.en.label'](),
				enText: m['examples.example1.en.text'](),
				djLabel: m['examples.example1.dj.label'](),
				djText: {
					latin: 'Fin a khoya, labas?',
					arabic: 'فينك يا خويا؟ لاباس؟'
				}
			},
			{
				enLabel: m['examples.example2.en.label'](),
				enText: m['examples.example2.en.text'](),
				djLabel: m['examples.example2.dj.label'](),
				djText: {
					latin: 'Lay 7afdek, finahowa a9rab restaurant?',
					arabic: 'الله يحفظك، فين هو أقرب ريستوران؟'
				}
			}
		]
	};

	const cta = {
		title: m['cta.title'](),
		text: m['cta.text'](),
		button: m['cta.button']()
	};
</script>

<section class="hero" style="--bg: url('{morocco}')">
	<div class="hero-content">
		<h1 class="hero-title">{hero.title}</h1>
		<p class="hero-text">{hero.text}</p>

		<div class="hero-actions">
			<a href={resolve('/translate')} class="hero-btn primary">
				{hero.ctaPrimary}
			</a>
			<a href={resolve('/about')} class="hero-btn secondary">
				{hero.ctaSecondary}
			</a>
		</div>
	</div>
</section>

<section class="value">
	<div class="value-content">
		<h2>{value.title}</h2>

		<ul>
			{#each value.items as item (item.title)}
				<li>
					<strong>{item.title}</strong>
					{item.text}
				</li>
			{/each}
		</ul>
	</div>
</section>

<section class="examples">
	<div class="examples-content">
		<div class="examples-text">
			<h2>{examples.title}</h2>
			<p>
				{examples.subtitle}
				<span style="font-weight: bold; color: var(--moroccan-green);">
					{examples.darija}:
				</span>
			</p>
		</div>

		<div class="examples-list">
			{#each examples.list as ex (ex.enText)}
				<div class="example">
					<h3>{ex.enLabel}</h3>
					<p>{ex.enText}</p>

					<h3>{ex.djLabel}</h3>
					<p>
						{ex.djText.latin}<br />
						<span class="ar">{ex.djText.arabic}</span>
					</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<section class="call-to-action">
	<div class="cta-content">
		<h2>{cta.title}</h2>
		<p>{cta.text}</p>
		<a href={resolve('/translate')} class="hero-btn primary">
			{cta.button}
		</a>
	</div>
</section>

<style>
	.hero {
		position: relative;
		width: 100%;
		min-height: 360px;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 2rem 0;
		text-align: center;
		overflow: hidden;
	}

	.hero::before {
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

	.hero::after {
		content: '';
		position: absolute;
		inset: 0;
		background: rgba(0, 0, 0, 0.45);
		z-index: 1;
	}

	.hero-content {
		position: relative;
		z-index: 2;
		max-width: 720px;
		color: white;
	}

	.hero-title {
		color: white;
		margin: 0 0 0.5rem;
	}

	.hero-text {
		color: #f1f1f1;
		margin-bottom: 1.5rem;
	}

	.hero-actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
	}

	.hero-btn {
		display: inline-block;
		padding: 0.75rem 2rem;
		border-radius: 8px;
		font-weight: 600;
		text-decoration: none;
		transition:
			transform 0.2s ease,
			background-color 0.3s ease,
			color 0.3s ease;
	}

	.hero-btn.primary {
		background: var(--moroccan-red);
		color: white;
	}

	.hero-btn.primary:hover {
		background: var(--moroccan-green);
		transform: translateY(-1px);
	}

	.hero-btn.secondary {
		border: 2px solid white;
		color: white;
	}

	.hero-btn.secondary:hover {
		background: white;
		color: var(--moroccan-green);
		transform: translateY(-1px);
	}

	.value {
		background-color: var(--moroccan-red);
		display: flex;
		width: 100%;
		justify-content: center;
		align-items: center;
		padding: 2rem 0;
	}

	.value-content {
		max-width: 720px;
		color: white;
		padding: 2rem 1.5rem;
	}

	.value-content h2 {
		text-align: center;
		margin-bottom: 1.5rem;
	}

	.value-content ul {
		list-style: none;
		padding: 0;
		margin: 1rem 0 0;
	}

	.value-content li {
		margin-bottom: 0.75rem;
		font-size: 1.1rem;
		background-color: white;
		color: black;
		padding: 1rem;
		border-radius: 10px;
		border-left: 8px solid var(--moroccan-green);
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	.value-content li:hover {
		transform: translateY(-3px);
		box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
	}

	.examples {
		background: #f8f8f8;
		width: 100%;
		display: flex;
		justify-content: center;
		box-sizing: border-box;
	}

	.examples-content {
		width: 100%;
		max-width: 800px;
		padding: 3rem 1.25rem;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2.5rem;
		box-sizing: border-box;
	}

	.examples-text {
		text-align: left;
	}

	@media (min-width: 769px) {
		.examples-text {
			display: flex;
			flex-direction: column;
			justify-content: center;
		}
	}

	.examples-list {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		padding-inline-end: 0.75rem;
		box-sizing: border-box;
	}

	.example {
		background: white;
		border-radius: 14px;
		padding: 1.5rem;
		box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
		border-top: 6px solid var(--moroccan-red);
		width: 100%;
		box-sizing: border-box;
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	.example:hover {
		transform: translateY(-4px);
		box-shadow: 0 14px 30px rgba(0, 0, 0, 0.15);
	}

	.example h3 {
		margin: 0.5rem 0 0.25rem;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #666;
	}

	.example p {
		margin: 0 0 0.75rem;
		font-size: 1.05rem;
	}

	.example h3:last-of-type + p {
		color: var(--moroccan-green);
		font-weight: 600;
	}

	@media (max-width: 768px) {
		.examples-content {
			grid-template-columns: 1fr;
		}

		.examples-text {
			text-align: center;
		}

		.examples-list {
			padding-inline-end: 0;
		}
	}

	.call-to-action {
		background: linear-gradient(135deg, var(--moroccan-red) 0%, #a01c1c 100%);
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 4rem 0;
		position: relative;
		overflow: hidden;
		box-sizing: border-box;
	}

	.call-to-action::before {
		content: '';
		position: absolute;
		inset: 0;
		background: radial-gradient(circle at top right, rgba(255, 255, 255, 0.1), transparent 60%);
		pointer-events: none;
	}

	.cta-content {
		position: relative;
		z-index: 1;
		max-width: 600px;
		text-align: center;
		color: white;
	}

	.cta-content h2 {
		font-size: 2.5rem;
		margin: 0 0 1rem;
		color: white;
	}

	.cta-content p {
		font-size: 1.2rem;
		margin: 0 0 2rem;
		color: rgba(255, 255, 255, 0.95);
	}

	.cta-content .hero-btn {
		font-size: 1.1rem;
		padding: 1rem 3rem;
		background: white;
		color: var(--moroccan-red);
		box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
	}

	.cta-content .hero-btn:hover {
		background: var(--moroccan-green);
		color: white;
		transform: translateY(-3px);
		box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
	}

	@media (max-width: 768px) {
		.cta-content h2 {
			font-size: 2rem;
		}

		.cta-content p {
			font-size: 1.05rem;
		}
	}
</style>
