import java.util.Scanner;

public class NonPrinc{
	public static void main(String args[])
	{
		Scanner sc = new Scanner(System.in);
		int a[][],i,j,sum=0;
		a= new int[3][3];
		for(i=0;i<3;i++)
		{
			for(j=0;j<3;j++)
			{
				a[i][j]=sc.nextInt();
			}
		}
		System.out.println("Non diagonal elements are:");
		for(i=0;i<3;i++)
		{
			for(j=0;j<3;j++)
			{
				if((i==j)|| (j==3-i-1))
				continue;
					System.out.print(a[i][j]+"\t");
					sum+=a[i][j];
			}
		}
		System.out.println("\nSum of numbers is:"+sum);
	}
}