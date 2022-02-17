#include <iostream>
#include <boost/array.hpp>
#include <boost/numeric/odeint.hpp>
#include <string>
#include <fstream>


using namespace std;
using namespace boost::numeric::odeint;


double b1 = 0.5; //Infectiousness
double n1 = 0.333; //Recoveries (high -> shorter sickness lenght)
double b2 = 0.5; //Infectiousness
double n2 = 0.333; //Recoveries (high -> shorter sickness lenght)
double male_pop = 40000000;
double female_pop = 40000000;
double male_init = 1;
double female_init = 1;

ofstream csvout("si.csv");

typedef boost::array< double , 4 > state_type;

void si( const state_type &x , state_type &dxdt , double t )
{
    dxdt[0] = -b1*x[0]*x[3]+n1*x[1];
    dxdt[1] = b1*x[0]*x[3]-n1*x[1];
    dxdt[2] = -b2*x[2]*x[1]+n2*x[3];
    dxdt[3] = b2*x[2]*x[1]-n2*x[3];
}

void write_si( const state_type &x , const double t )
{
    csvout << t << '\t' << x[0] << '\t' << x[2] << '\t' << x[1] << '\t' << x[3] << "\n";
}

int main(int argc,char* argv[])
{
    //Command line input: male population, female population, initial male cases, initial female cases,
    //                    infectiousness, recovery rate

    bool silent = false;
    if(argc==1){
    }else if(argc==9){
    male_pop = atof(argv[1]);
    female_pop = atof(argv[2]);
    male_init = atof(argv[3]);
    female_init = atof(argv[4]);

    b1 = atof(argv[5]);
    b2 = atof(argv[6]);
    n1 = atof(argv[7]);
    n2 = atof(argv[8]);

    }else{
    cout<<"Error, please either specify all or no arguments in the command line!\n";
    return -1;
    }

    double male_init_inf = male_init/male_pop;
    double male_init_susc = 1 - male_init_inf;
    double female_init_inf = female_init/female_pop;
    double female_init_susc = 1 - female_init_inf;

    runge_kutta_fehlberg78< state_type > stepper;
    state_type x = { male_init_susc , male_init_inf , female_init_susc , female_init_inf }; // initial conditions
    integrate_const( stepper , si , x , 1.0 , 600.0 , 1.0 , write_si );
    
    csvout.close();
}
