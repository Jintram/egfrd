#if !defined( __GREENSFUNCTION_HPP )
#define __GREENSFUNCTION_HPP

#include "Defs.hpp"

class GreensFunction
{
public:
    enum EventKind
    {
        IV_ESCAPE,
        IV_REACTION
    };

public:
    GreensFunction( const Real D )
      : D( D ) {}
  
    // needs virtual because of inheritance
    // made abstract because functions only as base
    virtual ~GreensFunction() = 0;
  
    Real getD() const
    {
        return this->D;
    }

protected:
    const Real D;
};

#endif // __GREENSFUNCTION_HPP
