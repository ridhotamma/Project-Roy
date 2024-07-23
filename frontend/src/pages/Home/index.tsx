import { LinkButton } from "../../components/button";

export function Home() {
  return (
    <div class='min-h-screen flex flex-col gap-4 justify-center items-center'>
      <h3 class='text-2xl mt-2'>ProjectRoy Home</h3>
      <a
        href={'/login'}
        class='w-full bg-blue-500 text-white p-2 rounded-lg text-center'
      >
        Login
      </a>
    </div>
  );
}
