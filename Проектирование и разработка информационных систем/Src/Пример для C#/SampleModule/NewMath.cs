using System.Linq;

namespace SampleModule
{
	/// <summary> Класс математических функций </summary>
	public class NewMath
	{
		/// <summary> Суммирование номеров</summary>
		/// <param name="numbers"> номера </param>
		/// <returns></returns>
		public int SumNumbers(params int[] numbers)
		{
			return numbers.Sum();
		}
	}
}
