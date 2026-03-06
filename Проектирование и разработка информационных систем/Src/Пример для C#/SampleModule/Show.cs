using System;

namespace SampleModule
{
	/// <summary> Класс отображения данных </summary>
	public class Show
	{
		/// <summary> Отображения множества чисел </summary>
		/// <param name="numbers"> Числа </param>
		public void ShowNumbers(params int[] numbers)
		{
			foreach (int number in numbers)
			{
				Console.WriteLine(number);
			}
		}
	}
}
