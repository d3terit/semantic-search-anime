import { useEffect, useState } from 'react';
import './Counter.css';
// import * as animeflv from 'animeflv-api';
// import { searchAnimesByFilter } from 'animeflv-api';

export default function Counter({
	children,
	count: initialCount,
}: {
	children: JSX.Element;
	count: number;
}) {
	const [count, setCount] = useState(initialCount);
	const add = () => setCount((i) => i + 1);
	const subtract = () => setCount((i) => i - 1);
	// searchAnimesByFilter({

	// }).then((result) => {
	// 	console.log(result);
	// })
	// post request to http://127.0.0.1:5000, send {query: ""}
	useEffect(() => {
		fetch('http://127.0.0.1:5000/semantic-search', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ query: 'armas blindadas con forma humanoide conocidas como "Titatonostrider"' }),
		})
			.then((response) => response.json())
			.then((data) => {
				console.log('Success:', data);
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	})
	return (
		<>
			<div className="counter">
				<button onClick={subtract}>-</button>
				<pre>{count}</pre>
				<button onClick={add}>+</button>
			</div>
			<div className="counter-message">{children}</div>
		</>
	);
}
