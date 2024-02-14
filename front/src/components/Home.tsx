import { useState } from "react";
import './Home.css';

const page_url = 'https://www3.animeflv.net/'
const url = 'http://127.0.0.1:5000/semantic-search'

const Home = () => {
    const [animes, setAnimes] = useState<any[]>([]);
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
            .then((data) => setAnimes(data))
            .catch((error) => {
                console.error('Error:', error);
            });
    }
    return (
        <section className="home">
            <article className="card-search">
                <header>
                    <h1><span style={{color: "#3ecf8e"}}>[Embeddings]</span> en la búsqueda de <span style={{color: "#db6c08"}}>animes.</span></h1>
                    <section>
                        <a style={{background: "#db6c08"}} href={page_url} target="_blank">Animeflv</a>
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
                        <input type="number" max={100} min={1} onChange={handleChange} id="match_count" value={query.match_count} />
                    </span>
                    <button onClick={handleSubmit}>Buscar</button>
                </footer>
            </article>
            {!!animes.length &&
                <article className="card-results">
                    <header>
                        <h1>Resultados</h1>
                    </header>
                    <section>
                        {animes.map((anime, index) => (
                            <div key={index} className="card-anime" onClick={() => setCurrentAnime(anime.title)}>
                                <span className="similarity">{(anime.similarity*100).toFixed(1)}%</span>
                                <img src={page_url + anime.cover} alt={anime.title} />
                                <h2>{anime.title}</h2>
                                <p>{anime.description}</p>
                                <a href={page_url + "anime/" + anime.url} target="_blank">Ver anime</a>
                            </div>
                        ))}
                    </section>
                </article>
            }
        </section>
    )
}

export default Home;