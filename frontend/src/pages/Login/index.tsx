import React from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';

interface IFormInput {
  username: string;
  password: string;
}

const validationSchema = Yup.object().shape({
  username: Yup.string().required('Username is required'),
  password: Yup.string().required('Password is required'),
});

export const Login: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<IFormInput>({
    resolver: yupResolver(validationSchema) as any,
  });

  const onSubmit: SubmitHandler<IFormInput> = (data) => {
    console.log(data);
  };

  return (
    <div className='min-h-screen flex items-center justify-center'>
      <div className='bg-white p-8 rounded-lg shadow-lg w-96'>
        <h2 className='text-2xl font-bold mb-6 text-gray-800'>Login</h2>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className='mb-4'>
            <label className='block text-gray-700'>Username</label>
            <input
              {...register('username')}
              className={`mt-1 p-2 w-full border bg-white ${
                errors.username ? 'border-red-500' : 'border-gray-300'
              } rounded-lg`}
              type='text'
            />
            {errors.username && (
              <span className='text-red-500 text-sm'>
                {errors.username.message}
              </span>
            )}
          </div>
          <div className='mb-6'>
            <label className='block text-gray-700'>Password</label>
            <input
              {...register('password')}
              className={`mt-1 p-2 w-full border bg-white ${
                errors.password ? 'border-red-500' : 'border-gray-300'
              } rounded-lg`}
              type='password'
            />
            {errors.password && (
              <span className='text-red-500 text-sm'>
                {errors.password.message}
              </span>
            )}
          </div>
          <button
            type='submit'
            className='w-full bg-blue-500 text-white p-2 rounded-lg'
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
};
