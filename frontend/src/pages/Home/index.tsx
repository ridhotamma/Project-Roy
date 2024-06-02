import { useEffect } from 'preact/hooks';

export function Home() {
  useEffect(() => {
    fetch('http://localhost:8000/ping')
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((err) => console.error(err));
  });

  return (
    <div class='min-h-screen w-full flex justify-center items-center'>
      <p class='text-center'>Index page</p>
    </div>
  );
}
