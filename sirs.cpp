#include <iostream>
#include <boost/array.hpp>
#include <boost/numeric/odeint.hpp>
#include <string>
#include <fstream>


using namespace std;
using namespace boost::numeric::odeint;


double b = 0.5; //Infectiousness
double m = 0.01; //Immunity loss
double n = 0.333; //Recoveries (high -> shorter sickness lenght)
double pop = 80000000;
double init = 1;

ofstream csvout("sirs.csv");

typedef boost::array< double , 3 > state_type;

void sirs( const state_type &x , state_type &dxdt , double t )
{
    dxdt[0] = -b*x[0]*x[1]+m*x[2];
    dxdt[1] = b*x[0]*x[1]-n*x[1];
    dxdt[2] = n*x[1]-m*x[2];
}

void write_sirs( const state_type &x , const double t )
{
    csvout << t << '\t' << x[0] << '\t' << x[1] << '\t' << x[2] << "\n";
}

int main(int argc,char* argv[])
{
    //Command line input: population, initial cases, infectiousness,
    //                    immunity loss, recovery rate

    bool silent = false;
    if(argc==1){
    }else if(argc==6){
    pop = atof(argv[1]);
    init = atof(argv[2]);

    b = atof(argv[3]);
    m = atof(argv[4]);
    n = atof(argv[5]);

    silent = true;
    }else{
    cout<<"Error, please either specify all or no arguments in the command line!\n";
    return -1;
    }

    string inp;
    while(!silent){
        cout<<"Do you want to load default parameters? [y/n] \n";
        cin>>inp;
        cout<<"\n";

        if(inp=="n"){
            cout<<"Population size: ";
            cin>>pop;
            cout<<"Initial cases: ";
            cin>>init;
            cout<<"Infectiousness (beta): ";
            cin>>b;
            cout<<"Recovery rate (nu): ";
            cin>>n;
            cout<<"Immunity loss (mu): ";
            cin>>m;

            silent = true;
        }else if(inp!="y"){
            cout<<"Invalid input\n\n";
        }else{
            cout<<"Running with default parameters\n";
            cout<<"\nPopulation size: "<<pop;
            cout<<"\nInitial cases: "<<init;
            cout<<"\nInfectiousness (beta): "<<b;
            cout<<"\nRecovery rate (nu): "<<n;
            cout<<"\nImmunity loss (mu): "<<m;
            silent=true;
        }
    }
    

    double init_inf = init/pop;
    double init_susc = 1 - init_inf;
    double rec = 0;
    runge_kutta_fehlberg78< state_type > stepper;
    state_type x = { init_susc , init_inf , rec }; // initial conditions
    integrate_const( stepper , sirs , x , 1.0 , 600.0 , 1.0 , write_sirs );
    
    csvout.close();
}
