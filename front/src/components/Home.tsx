import { useState } from "react";
import './Home.css';

const url = 'http://127.0.0.1:5000/semantic-search'

const Home = () => {
    const [currentAnime, setCurrentAnime] = useState<string | null>(null);
    const [query, setQuery] = useState<{ match_threshold: number, match_count: number}>({ match_threshold: 50, match_count: 5});
    const handleChange = (e: any) => {
        const { id, value } = e.target;
        setQuery({ ...query, [id]: value });
    }
    const handleSubmit = () => {
        const search = (document.getElementById('search') as HTMLInputElement).innerText;
        if (search === '') return;
        let data = {
            query: search,
            match_threshold: query.match_threshold / 100,
            match_count: query.match_count
        }
        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
    return (
        <section className="home">
            <article className="card-search">
                <header>
                    <h1>Embeddings en la búsqueda de <span style={{color: "#3ecf8e"}}>animes.</span></h1>
                    <section>
                        <a style={{background: "#db6c08"}} href="https://www3.animeflv.net/" target="_blank">Animeflv</a>
                        <a style={{background: "#37996b"}} href="https://supabase.com/" target="_blank">Supabase</a>
                    </section>
                </header>
                <p id="search" contentEditable></p>
                <footer>
                    <span>
                        <label htmlFor="match_threshold">Threshold</label>
                        <input type="number" max={100} min={0} onChange={handleChange} id="match_threshold" value={query.match_threshold} />
                    </span>
                    <span>
                        <label htmlFor="match_count">Resultados</label>
                        <input type="number" max={12} min={1} onChange={handleChange} id="match_count" value={query.match_count} />
                    </span>
                    <button onClick={handleSubmit}>Buscar</button>
                </footer>
            </article>
        </section>
    )
}

export default Home;