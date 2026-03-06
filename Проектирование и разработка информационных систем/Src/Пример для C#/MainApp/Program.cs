using SampleModule;

namespace MainApp
{
	internal class Program
	{
		/// <summary> Запуск главного приложения </summary>
		/// <param name="args"> Параметры </param>
		static void Main(string[] args)
		{
			var newMath = new NewMath();
			var show = new Show();

			var reult_1 = newMath.SumNumbers(new int[5] { 1, 2, 3, 4, 5 });

			var reult_2 = newMath.SumNumbers(new int[5] { 55, 66, 77, 88, 99 });

			show.ShowNumbers(reult_1, reult_2);
		}
	}
}
